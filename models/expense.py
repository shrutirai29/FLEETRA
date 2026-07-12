from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FleetraExpense(models.Model):
    _name = "fleetra.expense"
    _description = "Fleetra Operational Expense"
    _order = "date desc, id desc"

    name = fields.Char(
        string="Expense Description",
        required=True,
    )

    vehicle_id = fields.Many2one(
        "fleetra.vehicle",
        string="Vehicle",
        required=True,
    )

    trip_id = fields.Many2one(
        "fleetra.trip",
        string="Trip",
    )

    expense_type = fields.Selection(
        [
            ("toll", "Toll"),
            ("parking", "Parking"),
            ("driver_allowance", "Driver Allowance"),
            ("insurance", "Insurance"),
            ("fine", "Fine / Penalty"),
            ("permit", "Permit / Registration"),
            ("other", "Other"),
        ],
        string="Expense Type",
        required=True,
    )

    amount = fields.Monetary(
        string="Amount",
        currency_field="currency_id",
        required=True,
    )

    date = fields.Date(
        string="Expense Date",
        default=fields.Date.context_today,
        required=True,
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
    )

    # ---------------------------------------------------------
    # ONCHANGE
    # ---------------------------------------------------------

    @api.onchange("vehicle_id")
    def _onchange_vehicle_id(self):
        for expense in self:
            if (
                expense.trip_id
                and expense.trip_id.vehicle_id != expense.vehicle_id
            ):
                expense.trip_id = False

    # ---------------------------------------------------------
    # CONSTRAINTS
    # ---------------------------------------------------------

    @api.constrains("amount")
    def _check_amount(self):
        for expense in self:
            if expense.amount <= 0:
                raise ValidationError(
                    "Expense amount must be greater than zero."
                )

    @api.constrains("vehicle_id", "trip_id")
    def _check_trip_vehicle(self):
        for expense in self:
            if (
                expense.trip_id
                and expense.trip_id.vehicle_id != expense.vehicle_id
            ):
                raise ValidationError(
                    "The selected trip does not belong to "
                    "the selected vehicle."
                )