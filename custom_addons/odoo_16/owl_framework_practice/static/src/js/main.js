/** @odoo-module **/

import { whenReady,mount } from "@odoo/owl";
import { ClickCounter } from "./click_counter";

console.log("main.js: JavaScript execution started.");

whenReady(() => {
    const app = document.getElementById("app");
    if (app) {
        console.log("main.js: Mounting ClickCounter component.");
        // Use the Owl component mounting method
        mount(ClickCounter,app);
    } else {
        console.error("main.js: Mounting point #app not found!");
    }
});
