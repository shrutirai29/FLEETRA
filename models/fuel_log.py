from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FleetraFuelLog(models.Model):
    _name = "fleetra.fuel.log"
    _description = "Fleetra Fuel Log"
    _order = "date desc, id desc"

    vehicle_id = fields.Many2one(
        "fleetra.vehicle",
        string="Vehicle",
        required=True
    )

    trip_id = fields.Many2one(
        "fleetra.trip",
        string="Trip",
        domain="[('state', '=', 'completed')]"
    )

    liters = fields.Float(
        string="Fuel (Litres)",
        required=True
    )

    cost = fields.Monetary(
        string="Fuel Cost",
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

    fuel_efficiency = fields.Float(
        string="Fuel Efficiency (KM/L)",
        compute="_compute_fuel_efficiency"
    )

    @api.depends("liters", "trip_id.planned_distance")
    def _compute_fuel_efficiency(self):
        for log in self:
            if log.trip_id and log.liters > 0:
                log.fuel_efficiency = (
                    log.trip_id.planned_distance / log.liters
                )
            else:
                log.fuel_efficiency = 0.0

    @api.constrains("liters")
    def _check_liters(self):
        for log in self:
            if log.liters <= 0:
                raise ValidationError(
                    "Fuel quantity must be greater than 0 litres."
                )

    @api.constrains("cost")
    def _check_cost(self):
        for log in self:
            if log.cost < 0:
                raise ValidationError(
                    "Fuel cost cannot be negative."
                )

    @api.constrains("vehicle_id", "trip_id")
    def _check_trip_vehicle(self):
        for log in self:
            if (
                log.trip_id
                and log.trip_id.vehicle_id != log.vehicle_id
            ):
                raise ValidationError(
                    "Selected trip does not belong to the selected vehicle."
                )