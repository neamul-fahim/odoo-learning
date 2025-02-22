/** @odoo-module **/

import { Component, xml } from "@odoo/owl";

export const VendorDashboardTemplate = xml/* xml */ `
    <t t-name="vendor_dashboard.vendorDashboard_template">

            <t t-if="all_projects.value.length">
            <ProjectList all_projects="all_projects.value"/>
            </t>
            <t t-else="">
            <p>No projects found.</p>
            </t>

    </t>
`;