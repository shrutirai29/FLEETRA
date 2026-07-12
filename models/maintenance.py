from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class FleetraMaintenance(models.Model):
    _name = "fleetra.maintenance"
    _description = "Fleetra Vehicle Maintenance"
    _order = "start_date desc, id desc"

    name = fields.Char(
        string="Maintenance Reference",
        required=True,
        default="New",
        readonly=True,
        copy=False,
    )

    vehicle_id = fields.Many2one(
        "fleetra.vehicle",
        string="Vehicle",
        required=True,
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
        required=True,
    )

    description = fields.Text(
        string="Service Description",
    )

    start_date = fields.Date(
        string="Start Date",
        default=fields.Date.context_today,
        required=True,
    )

    end_date = fields.Date(
        string="Completion Date",
        readonly=True,
    )

    cost = fields.Monetary(
        string="Maintenance Cost",
        currency_field="currency_id",
        default=0.0,
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
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
        required=True,
    )

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code(
                        "fleetra.maintenance"
                    )
                    or "New"
                )

        return super().create(vals_list)

    # ---------------------------------------------------------
    # CONSTRAINTS
    # ---------------------------------------------------------

    @api.constrains("cost")
    def _check_cost(self):
        for maintenance in self:
            if maintenance.cost < 0:
                raise ValidationError(
                    "Maintenance cost cannot be negative."
                )

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for maintenance in self:
            if (
                maintenance.start_date
                and maintenance.end_date
                and maintenance.end_date
                < maintenance.start_date
            ):
                raise ValidationError(
                    "Completion date cannot be before the start date."
                )

    @api.constrains("vehicle_id", "state")
    def _check_active_maintenance(self):
        for maintenance in self:
            if (
                maintenance.vehicle_id
                and maintenance.state == "active"
            ):
                duplicate = self.search_count([
                    (
                        "vehicle_id",
                        "=",
                        maintenance.vehicle_id.id,
                    ),
                    ("state", "=", "active"),
                    ("id", "!=", maintenance.id),
                ])

                if duplicate:
                    raise ValidationError(
                        "This vehicle already has an active "
                        "maintenance record."
                    )

    # ---------------------------------------------------------
    # START MAINTENANCE
    # ---------------------------------------------------------

    def action_start_maintenance(self):
        for maintenance in self:

            if maintenance.state != "draft":
                raise UserError(
                    "Only draft maintenance records can be started."
                )

            if not maintenance.vehicle_id:
                raise UserError(
                    "Please select a vehicle."
                )

            vehicle = maintenance.vehicle_id

            if vehicle.status == "on_trip":
                raise UserError(
                    "This vehicle is currently on a trip and "
                    "cannot enter maintenance."
                )

            if vehicle.status == "retired":
                raise UserError(
                    "A retired vehicle cannot enter maintenance."
                )

            if vehicle.status == "in_shop":
                raise UserError(
                    "This vehicle is already in maintenance."
                )

            if vehicle.status != "available":
                raise UserError(
                    "Only available vehicles can enter maintenance."
                )

            vehicle.write({
                "status": "in_shop",
            })

            maintenance.write({
                "state": "active",
            })

        return True

    # ---------------------------------------------------------
    # CLOSE MAINTENANCE
    # ---------------------------------------------------------

    def action_close_maintenance(self):
        for maintenance in self:

            if maintenance.state != "active":
                raise UserError(
                    "Only active maintenance records can be completed."
                )

            if maintenance.cost <= 0:
                raise UserError(
                    "Please enter the maintenance cost "
                    "before completing maintenance."
                )

            if not maintenance.description:
                raise UserError(
                    "Please enter the service description "
                    "before completing maintenance."
                )

            maintenance.write({
                "end_date": fields.Date.context_today(self),
                "state": "closed",
            })

            if maintenance.vehicle_id.status != "retired":
                maintenance.vehicle_id.write({
                    "status": "available",
                })

        return True

    # ---------------------------------------------------------
    # CANCEL MAINTENANCE
    # ---------------------------------------------------------

    def action_cancel(self):
        for maintenance in self:

            if maintenance.state == "closed":
                raise UserError(
                    "Completed maintenance records cannot be cancelled."
                )

            if maintenance.state == "cancelled":
                raise UserError(
                    "This maintenance record is already cancelled."
                )

            if (
                maintenance.state == "active"
                and maintenance.vehicle_id.status != "retired"
            ):
                maintenance.vehicle_id.write({
                    "status": "available",
                })

            maintenance.write({
                "state": "cancelled",
            })

        return True