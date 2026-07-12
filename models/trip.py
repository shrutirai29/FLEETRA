from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class FleetraTrip(models.Model):
    _name = "fleetra.trip"
    _description = "Fleetra Trip"
    _order = "id desc"

    name = fields.Char(
        string="Trip Reference",
        required=True,
        copy=False,
        default="New",
    )

    source = fields.Char(
        string="Source",
        required=True,
    )

    destination = fields.Char(
        string="Destination",
        required=True,
    )

    cargo_weight = fields.Float(
        string="Cargo Weight",
        required=True,
    )

    vehicle_id = fields.Many2one(
        "fleetra.vehicle",
        string="Vehicle",
        required=True,
    )

    driver_id = fields.Many2one(
        "fleetra.driver",
        string="Driver",
        required=True,
    )

    planned_distance = fields.Float(
        string="Planned Distance (KM)",
        required=True,
    )

    capacity_utilization = fields.Float(
        string="Capacity Utilization (%)",
        compute="_compute_capacity_utilization",
        store=True,
    )

    current_odometer = fields.Float(
        string="Current Odometer (KM)",
        related="vehicle_id.odometer",
        readonly=True,
    )

    expected_final_odometer = fields.Float(
        string="Expected Final Odometer (KM)",
        compute="_compute_expected_final_odometer",
    )

    final_odometer = fields.Float(
        string="Final Odometer (KM)",
    )

    fuel_consumed = fields.Float(
        string="Fuel Consumed (L)",
    )

    fuel_cost = fields.Monetary(
        string="Fuel Cost",
        currency_field="currency_id",
    )

    revenue = fields.Monetary(
        string="Revenue",
        currency_field="currency_id",
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("dispatched", "Dispatched"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        required=True,
    )

    # ---------------------------------------------------------
    # COMPUTE METHODS
    # ---------------------------------------------------------

    @api.depends(
        "cargo_weight",
        "vehicle_id",
        "vehicle_id.max_load_capacity",
    )
    def _compute_capacity_utilization(self):
        for trip in self:
            if (
                trip.vehicle_id
                and trip.vehicle_id.max_load_capacity > 0
            ):
                trip.capacity_utilization = (
                    trip.cargo_weight
                    / trip.vehicle_id.max_load_capacity
                ) * 100
            else:
                trip.capacity_utilization = 0.0

    @api.depends(
        "vehicle_id",
        "vehicle_id.odometer",
        "planned_distance",
    )
    def _compute_expected_final_odometer(self):
        for trip in self:
            if trip.vehicle_id:
                trip.expected_final_odometer = (
                    trip.vehicle_id.odometer
                    + trip.planned_distance
                )
            else:
                trip.expected_final_odometer = 0.0

    # ---------------------------------------------------------
    # ONCHANGE
    # ---------------------------------------------------------

    @api.onchange("cargo_weight")
    def _onchange_cargo_weight(self):
        for trip in self:
            if (
                trip.vehicle_id
                and trip.cargo_weight > 0
                and trip.cargo_weight
                > trip.vehicle_id.max_load_capacity
            ):
                trip.vehicle_id = False

                return {
                    "warning": {
                        "title": "Vehicle Capacity Warning",
                        "message": (
                            "The selected vehicle cannot carry this cargo. "
                            "Please select a vehicle with sufficient capacity."
                        ),
                    }
                }

    @api.onchange("vehicle_id", "planned_distance")
    def _onchange_final_odometer(self):
        for trip in self:
            if (
                trip.vehicle_id
                and trip.planned_distance > 0
                and trip.state == "draft"
            ):
                trip.final_odometer = (
                    trip.vehicle_id.odometer
                    + trip.planned_distance
                )

    # ---------------------------------------------------------
    # CONSTRAINTS
    # ---------------------------------------------------------

    @api.constrains("cargo_weight", "vehicle_id")
    def _check_vehicle_capacity(self):
        for trip in self:
            if trip.cargo_weight <= 0:
                raise ValidationError(
                    "Cargo weight must be greater than zero."
                )

            if (
                trip.vehicle_id
                and trip.cargo_weight
                > trip.vehicle_id.max_load_capacity
            ):
                raise ValidationError(
                    "Selected vehicle cannot carry this cargo weight."
                )

    @api.constrains("planned_distance")
    def _check_planned_distance(self):
        for trip in self:
            if trip.planned_distance <= 0:
                raise ValidationError(
                    "Planned distance must be greater than zero."
                )

    # ---------------------------------------------------------
    # DISPATCH
    # ---------------------------------------------------------

    def action_dispatch(self):
        for trip in self:
            if trip.state != "draft":
                raise UserError(
                    "Only draft trips can be dispatched."
                )

            if trip.cargo_weight <= 0:
                raise UserError(
                    "Please enter a valid cargo weight."
                )

            if not trip.vehicle_id:
                raise UserError(
                    "Please select a suitable vehicle."
                )

            if (
                trip.cargo_weight
                > trip.vehicle_id.max_load_capacity
            ):
                raise UserError(
                    "Selected vehicle does not have sufficient capacity."
                )

            if trip.vehicle_id.status != "available":
                raise UserError(
                    "Selected vehicle is currently unavailable."
                )

            if not trip.driver_id:
                raise UserError(
                    "Please select a driver."
                )

            if trip.driver_id.status != "available":
                raise UserError(
                    "Selected driver is currently unavailable."
                )

            if trip.driver_id.license_status == "expired":
                raise UserError(
                    "Selected driver's license has expired."
                )

            trip.vehicle_id.status = "on_trip"
            trip.driver_id.status = "on_trip"
            trip.state = "dispatched"

        return True

    # ---------------------------------------------------------
    # COMPLETE
    # ---------------------------------------------------------

    def action_complete(self):
        for trip in self:
            if trip.state != "dispatched":
                raise UserError(
                    "Only dispatched trips can be completed."
                )

            if trip.final_odometer <= 0:
                raise UserError(
                    "Please enter the final odometer."
                )

            if trip.final_odometer < trip.vehicle_id.odometer:
                raise UserError(
                    f"Final odometer cannot be less than "
                    f"{trip.vehicle_id.odometer:.2f} KM."
                )

            if trip.fuel_consumed <= 0:
                raise UserError(
                    "Please enter fuel consumed."
                )

            if trip.fuel_cost <= 0:
                raise UserError(
                    "Please enter the total fuel cost."
                )

            existing_fuel_log = self.env[
                "fleetra.fuel.log"
            ].search([
                ("trip_id", "=", trip.id)
            ], limit=1)

            if not existing_fuel_log:
                self.env["fleetra.fuel.log"].create({
                    "vehicle_id": trip.vehicle_id.id,
                    "trip_id": trip.id,
                    "liters": trip.fuel_consumed,
                    "cost": trip.fuel_cost,
                    "date": fields.Date.context_today(self),
                })

            trip.vehicle_id.write({
                "status": "available",
                "odometer": trip.final_odometer,
            })

            trip.driver_id.write({
                "status": "available",
            })

            trip.state = "completed"

        return True

    # ---------------------------------------------------------
    # CANCEL
    # ---------------------------------------------------------

    def action_cancel(self):
        for trip in self:
            if trip.state == "completed":
                raise UserError(
                    "Completed trips cannot be cancelled."
                )

            if trip.state == "dispatched":
                trip.vehicle_id.status = "available"
                trip.driver_id.status = "available"

            trip.state = "cancelled"

        return True

    # ---------------------------------------------------------
    # RESET
    # ---------------------------------------------------------

    def action_reset_draft(self):
        for trip in self:
            if trip.state != "cancelled":
                raise UserError(
                    "Only cancelled trips can be reset to draft."
                )

            trip.state = "draft"

        return True