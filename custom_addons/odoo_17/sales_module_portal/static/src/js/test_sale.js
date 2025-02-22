/** @odoo-module */
import { Component, useRef, onWillStart, useState, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";


// Define the simple Owl component
export class GreetingComponent extends Component {
  static template = xml`<div>Hello, welcome to my simple Owl component!</div>`;
}

registry.category("public_components").add("sales_module_portal.test_sale", GreetingComponent);
