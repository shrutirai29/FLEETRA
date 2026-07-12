from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FleetraExpense(models.Model):
    _name = "fleetra.expense"
    _description = "Fleetra Operational Expense"
    _order = "date desc, id desc"

    name = fields.Char(
        string="Description",
        required=True
    )

    vehicle_id = fields.Many2one(
        "fleetra.vehicle",
        string="Vehicle",
        required=True
    )

    trip_id = fields.Many2one(
        "fleetra.trip",
        string="Trip"
    )

    expense_type = fields.Selection(
        [
            ("toll", "Toll"),
            ("parking", "Parking"),
            ("repair", "Repair"),
            ("insurance", "Insurance"),
            ("other", "Other"),
        ],
        string="Expense Type",
        required=True
    )

    amount = fields.Monetary(
        string="Amount",
        required=True
    )

    date = fields.Date(
        string="Date",
        default=fields.Date.context_today,
        required=True
    )

    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id
    )

    @api.constrains("amount")
    def _check_amount(self):
        for expense in self:
            if expense.amount < 0:
                raise ValidationError(
                    "Expense amount cannot be negative."
                )

    @api.constrains("vehicle_id", "trip_id")
    def _check_trip_vehicle(self):
        for expense in self:
            if (
                expense.trip_id
                and expense.trip_id.vehicle_id != expense.vehicle_id
            ):
                raise ValidationError(
                    "Selected trip does not belong to the selected vehicle."
                )