from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class FleetraTrip(models.Model):
    _name = "fleetra.trip"
    _description = "Fleetra Transport Trip"
    _order = "id desc"

    name = fields.Char(
        string="Trip Reference",
        default="New",
        readonly=True,
        copy=False
    )

    source = fields.Char(
        string="Source",
        required=True
    )

    destination = fields.Char(
        string="Destination",
        required=True
    )

    vehicle_id = fields.Many2one(
        "fleetra.vehicle",
        string="Vehicle",
        required=True,
        domain="[('status', '=', 'available')]"
    )

    driver_id = fields.Many2one(
        "fleetra.driver",
        string="Driver",
        required=True,
        domain="[('status', '=', 'available'), ('license_status', '!=', 'expired')]"
    )

    cargo_weight = fields.Float(
        string="Cargo Weight (KG)",
        required=True
    )

    planned_distance = fields.Float(
        string="Planned Distance (KM)",
        required=True
    )

    final_odometer = fields.Float(
        string="Final Odometer (KM)"
    )

    fuel_consumed = fields.Float(
        string="Fuel Consumed (L)"
    )

    revenue = fields.Monetary(
        string="Trip Revenue"
    )

    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id
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
        required=True
    )

    capacity_utilization = fields.Float(
        string="Capacity Utilization (%)",
        compute="_compute_capacity_utilization"
    )

    @api.depends("cargo_weight", "vehicle_id")
    def _compute_capacity_utilization(self):
        for trip in self:
            if trip.vehicle_id and trip.vehicle_id.max_load_capacity:
                trip.capacity_utilization = (
                    trip.cargo_weight
                    / trip.vehicle_id.max_load_capacity
                ) * 100
            else:
                trip.capacity_utilization = 0

    @api.constrains("cargo_weight", "vehicle_id")
    def _check_cargo_capacity(self):
        for trip in self:
            if trip.cargo_weight <= 0:
                raise ValidationError(
                    "Cargo weight must be greater than 0 KG."
                )

            if (
                trip.vehicle_id
                and trip.cargo_weight
                > trip.vehicle_id.max_load_capacity
            ):
                exceeded = (
                    trip.cargo_weight
                    - trip.vehicle_id.max_load_capacity
                )

                raise ValidationError(
                    f"Capacity exceeded by {exceeded:.2f} KG. "
                    f"{trip.vehicle_id.name} can carry a maximum "
                    f"of {trip.vehicle_id.max_load_capacity:.2f} KG."
                )

    @api.constrains("planned_distance")
    def _check_planned_distance(self):
        for trip in self:
            if trip.planned_distance <= 0:
                raise ValidationError(
                    "Planned distance must be greater than 0 KM."
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "fleetra.trip"
                ) or "New"

        return super().create(vals_list)

    def action_dispatch(self):
        for trip in self:
            if trip.state != "draft":
                raise UserError(
                    "Only draft trips can be dispatched."
                )

            if trip.vehicle_id.status != "available":
                raise UserError(
                    "Selected vehicle is not available."
                )

            if trip.driver_id.status != "available":
                raise UserError(
                    "Selected driver is not available."
                )

            if trip.driver_id.license_status == "expired":
                raise UserError(
                    "Driver license has expired. Assignment blocked."
                )

            if trip.driver_id.status == "suspended":
                raise UserError(
                    "Suspended drivers cannot be assigned to trips."
                )

            if trip.cargo_weight > trip.vehicle_id.max_load_capacity:
                raise UserError(
                    "Cargo weight exceeds vehicle capacity."
                )

            trip.vehicle_id.status = "on_trip"
            trip.driver_id.status = "on_trip"
            trip.state = "dispatched"

    def action_complete(self):
        for trip in self:
            if trip.state != "dispatched":
                raise UserError(
                    "Only dispatched trips can be completed."
                )

            if trip.final_odometer <= trip.vehicle_id.odometer:
                raise UserError(
                    "Final odometer must be greater than the current odometer."
                )

            if trip.fuel_consumed <= 0:
                raise UserError(
                    "Fuel consumed must be greater than 0 litres."
                )

            trip.vehicle_id.odometer = trip.final_odometer
            trip.vehicle_id.status = "available"
            trip.driver_id.status = "available"
            trip.state = "completed"

    def action_cancel(self):
        for trip in self:
            if trip.state not in ("draft", "dispatched"):
                raise UserError(
                    "Completed trips cannot be cancelled."
                )

            if trip.state == "dispatched":
                trip.vehicle_id.status = "available"
                trip.driver_id.status = "available"

            trip.state = "cancelled"

    def action_reset_draft(self):
        for trip in self:
            if trip.state != "cancelled":
                raise UserError(
                    "Only cancelled trips can be reset."
                )

            trip.state = "draft"