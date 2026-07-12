from datetime import date

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class FleetraDriver(models.Model):
    _name = "fleetra.driver"
    _description = "Fleetra Driver"
    _order = "name"

    name = fields.Char(
        string="Driver Name",
        required=True,
    )

    license_number = fields.Char(
        string="License Number",
        required=True,
        copy=False,
        index=True,
    )

    license_category = fields.Selection(
        [
            ("lmv", "LMV"),
            ("hmv", "HMV"),
            ("transport", "Transport"),
            ("commercial", "Commercial"),
        ],
        string="License Category",
        required=True,
    )

    license_expiry_date = fields.Date(
        string="License Expiry Date",
        required=True,
    )

    contact_number = fields.Char(
        string="Contact Number",
        required=True,
    )

    safety_score = fields.Float(
        string="Safety Score",
        default=100.0,
    )

    status = fields.Selection(
        [
            ("available", "Available"),
            ("on_trip", "On Trip"),
            ("off_duty", "Off Duty"),
            ("suspended", "Suspended"),
        ],
        string="Status",
        default="available",
        required=True,
    )

    license_status = fields.Selection(
        [
            ("valid", "Valid"),
            ("expiring", "Expiring Soon"),
            ("expired", "Expired"),
        ],
        string="License Status",
        compute="_compute_license_status",
        store=True,
    )

    _sql_constraints = [
        (
            "unique_license_number",
            "unique(license_number)",
            "Driver license number must be unique!",
        )
    ]

    @api.depends("license_expiry_date")
    def _compute_license_status(self):
        today = fields.Date.today()

        for driver in self:
            if not driver.license_expiry_date:
                driver.license_status = False
                continue

            days_remaining = (
                driver.license_expiry_date - today
            ).days

            if days_remaining < 0:
                driver.license_status = "expired"
            elif days_remaining <= 30:
                driver.license_status = "expiring"
            else:
                driver.license_status = "valid"

    @api.constrains("safety_score")
    def _check_safety_score(self):
        for driver in self:
            if not 0 <= driver.safety_score <= 100:
                raise ValidationError(
                    "Safety score must be between 0 and 100."
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("license_number"):
                vals["license_number"] = (
                    vals["license_number"]
                    .strip()
                    .upper()
                )

        return super().create(vals_list)

    def write(self, vals):
        if vals.get("license_number"):
            vals["license_number"] = (
                vals["license_number"]
                .strip()
                .upper()
            )

        return super().write(vals)