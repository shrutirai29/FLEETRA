from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FleetraVehicle(models.Model):
    _name = "fleetra.vehicle"
    _description = "Fleetra Vehicle"
    _order = "name"

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
        required=True
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
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
        default=True
    )

    _sql_constraints = [
        (
            "unique_registration_number",
            "unique(registration_number)",
            "Vehicle registration number must be unique!"
        )
    ]

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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("registration_number"):
                vals["registration_number"] = (
                    vals["registration_number"].strip().upper()
                )

        return super().create(vals_list)

    def write(self, vals):
        if vals.get("registration_number"):
            vals["registration_number"] = (
                vals["registration_number"].strip().upper()
            )

        return super().write(vals)