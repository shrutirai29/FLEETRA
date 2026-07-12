from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FleetraVehicle(models.Model):
    _name = "fleetra.vehicle"
    _description = "Fleetra Vehicle"
    _order = "name"

    # ---------------------------------------------------------
    # BASIC VEHICLE INFORMATION
    # ---------------------------------------------------------

    name = fields.Char(
        string="Vehicle Name / Model",
        required=True
    )

    registration_number = fields.Char(
        string="Registration Number",
        required=True,
        copy=False,
        index=True
    )

    vehicle_type = fields.Selection(
        [
            ("van", "Van"),
            ("truck", "Truck"),
            ("bus", "Bus"),
            ("mini_truck", "Mini Truck"),
            ("other", "Other"),
        ],
        string="Vehicle Type",
        required=True
    )

    max_load_capacity = fields.Float(
        string="Maximum Load Capacity (KG)",
        required=True
    )

    odometer = fields.Float(
        string="Odometer (KM)",
        default=0.0
    )

    acquisition_cost = fields.Monetary(
        string="Acquisition Cost",
        required=True,
        currency_field="currency_id"
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id
    )

    region = fields.Char(
        string="Region"
    )

    status = fields.Selection(
        [
            ("available", "Available"),
            ("on_trip", "On Trip"),
            ("in_shop", "In Shop"),
            ("retired", "Retired"),
        ],
        string="Status",
        default="available",
        required=True
    )

    active = fields.Boolean(
        string="Active",
        default=True
    )

    # ---------------------------------------------------------
    # RELATIONSHIPS
    # ---------------------------------------------------------

    fuel_log_ids = fields.One2many(
        "fleetra.fuel.log",
        "vehicle_id",
        string="Fuel Logs"
    )

    maintenance_ids = fields.One2many(
        "fleetra.maintenance",
        "vehicle_id",
        string="Maintenance Records"
    )

    expense_ids = fields.One2many(
        "fleetra.expense",
        "vehicle_id",
        string="Expenses"
    )

    # ---------------------------------------------------------
    # OPERATIONAL COSTS
    # ---------------------------------------------------------

    total_fuel_cost = fields.Monetary(
        string="Total Fuel Cost",
        compute="_compute_operational_cost",
        currency_field="currency_id"
    )

    total_maintenance_cost = fields.Monetary(
        string="Total Maintenance Cost",
        compute="_compute_operational_cost",
        currency_field="currency_id"
    )

    total_other_expenses = fields.Monetary(
        string="Other Expenses",
        compute="_compute_operational_cost",
        currency_field="currency_id"
    )

    total_operational_cost = fields.Monetary(
        string="Operational Cost",
        compute="_compute_operational_cost",
        currency_field="currency_id"
    )

    # ---------------------------------------------------------
    # DATABASE CONSTRAINTS
    # ---------------------------------------------------------

    _sql_constraints = [
        (
            "unique_registration_number",
            "unique(registration_number)",
            "Vehicle registration number must be unique!"
        )
    ]

    # ---------------------------------------------------------
    # COMPUTED FIELDS
    # ---------------------------------------------------------

    @api.depends(
        "fuel_log_ids.cost",
        "maintenance_ids.cost",
        "maintenance_ids.state",
        "expense_ids.amount"
    )
    def _compute_operational_cost(self):
        for vehicle in self:

            vehicle.total_fuel_cost = sum(
                vehicle.fuel_log_ids.mapped("cost")
            )

            vehicle.total_maintenance_cost = sum(
                vehicle.maintenance_ids.filtered(
                    lambda maintenance: maintenance.state == "closed"
                ).mapped("cost")
            )

            vehicle.total_other_expenses = sum(
                vehicle.expense_ids.mapped("amount")
            )

            vehicle.total_operational_cost = (
                vehicle.total_fuel_cost
                + vehicle.total_maintenance_cost
                + vehicle.total_other_expenses
            )

    # ---------------------------------------------------------
    # VALIDATIONS
    # ---------------------------------------------------------

    @api.constrains("max_load_capacity")
    def _check_max_load_capacity(self):
        for vehicle in self:
            if vehicle.max_load_capacity <= 0:
                raise ValidationError(
                    "Maximum load capacity must be greater than 0 KG."
                )

    @api.constrains("odometer")
    def _check_odometer(self):
        for vehicle in self:
            if vehicle.odometer < 0:
                raise ValidationError(
                    "Odometer reading cannot be negative."
                )

    @api.constrains("acquisition_cost")
    def _check_acquisition_cost(self):
        for vehicle in self:
            if vehicle.acquisition_cost < 0:
                raise ValidationError(
                    "Acquisition cost cannot be negative."
                )

    # ---------------------------------------------------------
    # CREATE / UPDATE
    # ---------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("registration_number"):
                vals["registration_number"] = (
                    vals["registration_number"]
                    .strip()
                    .upper()
                )

        return super().create(vals_list)

    def write(self, vals):
        if vals.get("registration_number"):
            vals["registration_number"] = (
                vals["registration_number"]
                .strip()
                .upper()
            )

        return super().write(vals)