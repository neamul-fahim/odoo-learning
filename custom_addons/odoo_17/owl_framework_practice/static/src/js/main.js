/** @odoo-module **/

import { browser } from "@web/core/browser/browser";
import { mount } from "@odoo/owl";
import { ClickCounter } from "./click_counter";

// The following code ensures that owl mount the component when ready.
// `templates` contains templates contained in the bundles.
//
// In the mount options, it's also possible to add other interresting
// configuration: https://github.com/odoo/owl/blob/master/doc/reference/app.md#configuration
import { templates } from "@web/core/assets";

console.log("main.js: JavaScript execution started.");

owl.whenReady( () => {
    mount(ClickCounter, document.body, { templates, dev: true });
});


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

