/** @odoo-module **/

import { mount, loadFile } from "@odoo/owl";
import { VendorDashboard } from "./my_dashboard";

async function setup() {
    try {
        // Adjusted URL to point to static assets
        const templates = await loadFile('/web/static/src/vendor_dashboard/my_dashboard.xml');

        const env = { templates };

        mount(VendorDashboard, document.getElementById("vendor_dashboard_mount"), {
            env: env,
        });
    } catch (error) {
        console.error("Error loading templates:", error);
    }
}

setup();
//console.log("--------------Mounting------------load_vendor_dashboard.js");

//owl.whenReady( () => {
//console.log("--------------Mounting vendor_dashboard_mount component.");
//
//const app = document.getElementById("vendor_dashboard_mount");
//    if (app) {
//        console.log("main.js: Mounting ClickCounter component.");
//        // Use the Owl component mounting method
//        mount(VendorDashboard,app, { templates, dev: true });
//    } else {
//        console.error("main.js: Mounting point #app not found!");
//    }});


/**
 * This code is iterating over the cause property of an error object to console.error a string
 * containing the stack trace of the error and any errors that caused it.
 * @param {Event} ev
 */
function logError(ev) {
    ev.preventDefault();
    let error = ev ?.error || ev.reason;

    if (error.seen) {
        // If an error causes the mount to crash, Owl will reject the mount promise and throw the
        // error. Therefore, this if statement prevents the same error from appearing twice.
        return;
    }
    error.seen = true;

    let errorMessage = error.stack;
    while (error.cause) {
        errorMessage += "\nCaused by: "
        errorMessage += error.cause.stack;
        error = error.cause;
    }
    console.error(errorMessage);
}

browser.addEventListener("error", (ev) => {logError(ev)});
browser.addEventListener("unhandledrejection", (ev) => {logError(ev)});




























///** @odoo-module **/
//
//import { whenReady,mount } from "@odoo/owl";
//import { ClickCounter } from "./click_counter";
//
//console.log("main.js: JavaScript execution started.");
//
//whenReady(() => {
//    const app = document.getElementById("app");
//    if (app) {
//        console.log("main.js: Mounting ClickCounter component.");
//        // Use the Owl component mounting method
//        mount(ClickCounter,app);
//    } else {
//        console.error("main.js: Mounting point #app not found!");
//    }
//});

