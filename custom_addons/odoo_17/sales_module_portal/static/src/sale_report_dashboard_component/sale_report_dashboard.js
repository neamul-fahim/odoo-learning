/** @odoo-module */

import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import { Component, onWillStart, useRef, onMounted, onWillUnmount, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class SalesPieChart extends Component {
    static template = "sales_module_portal.sale_report_dashboard";

    setup() {
        this.rpc = useService("rpc");
        this.canvasRef = useRef("canvas");
        this.state = useState({
            totalSales: 0,
            confirmedOrders: 0,
            averageSalesValue: 0,
        });

        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        onMounted(() => {
            this.fetchSalesData();
        });
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    async fetchSalesData() {
        try {
            const result = await this.rpc('/sale_report_data');
            console.log('Sales Data:', result);

            // Set the fetched data in the component state
            this.state.totalSales = result.total_sales;
            this.state.confirmedOrders = result.confirmed_orders;
            this.state.averageSalesValue = result.average_sales_value;

            // Render the chart once the data is available
            this.renderChart();
        } catch (error) {
            console.error("Failed to fetch sales data", error);
        }
    }

    renderChart() {
        const labels = ["Total Sales", "Confirmed Orders", "Average Sales Value"];
        const data = [
            this.state.totalSales,
            this.state.confirmedOrders,
            this.state.averageSalesValue
        ];
        const color = labels.map((_, index) => getColor(index));

        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Sales Data Overview",
                        data: data,
                        backgroundColor: color,
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'right',
                    },
                },
            },
        });
    }
}

registry.category("public_components").add("sales_module_portal.sale_report_dashboard", SalesPieChart);
