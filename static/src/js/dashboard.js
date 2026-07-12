/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class FleetraDashboard extends Component {
    static template = "fleetra.FleetraDashboard";

    setup() {
        this.orm = useService("orm");

        this.state = useState({
            loading: true,
            data: {
                active_vehicles: 0,
                available_vehicles: 0,
                maintenance_vehicles: 0,
                active_trips: 0,
                pending_trips: 0,
                drivers_on_duty: 0,
                fleet_utilization: 0,
                operational_cost: 0,
            },
        });

        onWillStart(async () => {
            await this.loadDashboard();
        });
    }

    async loadDashboard() {
        this.state.loading = true;

        this.state.data = await this.orm.call(
            "fleetra.dashboard",
            "get_dashboard_data",
            []
        );

        this.state.loading = false;
    }
}

registry.category("actions").add(
    "fleetra_dashboard",
    FleetraDashboard
);