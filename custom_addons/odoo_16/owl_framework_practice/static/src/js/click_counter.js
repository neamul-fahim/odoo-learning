/** @odoo-module **/

import { Component,xml } from "@odoo/owl";

console.log("click_counter.js: ClickCounter component definition loaded.");

export class ClickCounter extends Component {
    static template = xml`<div>Simple ClickCounter Component</div>`;
}
