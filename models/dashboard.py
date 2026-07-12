from odoo import models, api


class FleetraDashboard(models.AbstractModel):
    _name = "fleetra.dashboard"
    _description = "Fleetra Dashboard"

    @api.model
    def get_dashboard_data(self):
        Vehicle = self.env["fleetra.vehicle"]
        Driver = self.env["fleetra.driver"]
        Trip = self.env["fleetra.trip"]

        total_vehicles = Vehicle.search_count([
            ("status", "!=", "retired")
        ])

        available_vehicles = Vehicle.search_count([
            ("status", "=", "available")
        ])

        vehicles_in_maintenance = Vehicle.search_count([
            ("status", "=", "in_shop")
        ])

        active_trips = Trip.search_count([
            ("state", "=", "dispatched")
        ])

        pending_trips = Trip.search_count([
            ("state", "=", "draft")
        ])

        drivers_on_duty = Driver.search_count([
            ("status", "in", ["available", "on_trip"])
        ])

        on_trip_vehicles = Vehicle.search_count([
            ("status", "=", "on_trip")
        ])

        fleet_utilization = 0.0

        if total_vehicles:
            fleet_utilization = (
                on_trip_vehicles / total_vehicles
            ) * 100

        vehicles = Vehicle.search([])

        total_operational_cost = sum(
            vehicles.mapped("total_operational_cost")
        )

        return {
            "active_vehicles": total_vehicles,
            "available_vehicles": available_vehicles,
            "maintenance_vehicles": vehicles_in_maintenance,
            "active_trips": active_trips,
            "pending_trips": pending_trips,
            "drivers_on_duty": drivers_on_duty,
            "fleet_utilization": round(fleet_utilization, 2),
            "operational_cost": total_operational_cost,
        }