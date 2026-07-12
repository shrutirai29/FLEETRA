from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class FleetraMaintenance(models.Model):
    _name = "fleetra.maintenance"
    _description = "Fleetra Vehicle Maintenance"
    _order = "start_date desc, id desc"

    name = fields.Char(
        string="Maintenance Reference",
        default="New",
        readonly=True,
        copy=False
    )

    vehicle_id = fields.Many2one(
        "fleetra.vehicle",
        string="Vehicle",
        required=True,
        domain="[('status', 'not in', ['on_trip', 'retired'])]"
    )

    service_type = fields.Selection(
        [
            ("oil_change", "Oil Change"),
            ("brake_repair", "Brake Repair"),
            ("tyre_service", "Tyre Service"),
            ("engine_service", "Engine Service"),
            ("inspection", "General Inspection"),
            ("other", "Other"),
        ],
        string="Service Type",
        required=True
    )

    description = fields.Text(
        string="Service Description"
    )

    start_date = fields.Date(
        string="Start Date",
        default=fields.Date.context_today,
        required=True
    )

    end_date = fields.Date(
        string="Completion Date"
    )

    cost = fields.Monetary(
        string="Maintenance Cost",
        default=0.0
    )

    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "In Progress"),
            ("closed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        required=True
    )

    @api.constrains("cost")
    def _check_cost(self):
        for maintenance in self:
            if maintenance.cost < 0:
                raise ValidationError(
                    "Maintenance cost cannot be negative."
                )

    @api.constrains("end_date", "start_date")
    def _check_dates(self):
        for maintenance in self:
            if (
                maintenance.end_date
                and maintenance.start_date
                and maintenance.end_date < maintenance.start_date
            ):
                raise ValidationError(
                    "Completion date cannot be before start date."
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "fleetra.maintenance"
                ) or "New"

        return super().create(vals_list)

    def action_start_maintenance(self):
        for maintenance in self:
            vehicle = maintenance.vehicle_id

            if maintenance.state != "draft":
                raise UserError(
                    "Only draft maintenance records can be started."
                )

            if vehicle.status == "on_trip":
                raise UserError(
                    "A vehicle currently on a trip cannot enter maintenance."
                )

            if vehicle.status == "retired":
                raise UserError(
                    "A retired vehicle cannot enter maintenance."
                )

            if vehicle.status == "in_shop":
                raise UserError(
                    "This vehicle is already in maintenance."
                )

            vehicle.status = "in_shop"
            maintenance.state = "active"

    def action_close_maintenance(self):
        for maintenance in self:
            if maintenance.state != "active":
                raise UserError(
                    "Only active maintenance records can be closed."
                )

            maintenance.end_date = fields.Date.context_today(self)
            maintenance.state = "closed"

            if maintenance.vehicle_id.status != "retired":
                maintenance.vehicle_id.status = "available"

    def action_cancel(self):
        for maintenance in self:
            if maintenance.state == "closed":
                raise UserError(
                    "Completed maintenance cannot be cancelled."
                )

            if (
                maintenance.state == "active"
                and maintenance.vehicle_id.status != "retired"
            ):
                maintenance.vehicle_id.status = "available"

            maintenance.state = "cancelled"