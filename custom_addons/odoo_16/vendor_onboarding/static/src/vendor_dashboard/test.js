/** @odoo-module **/

import { Component, useRef, onWillStart, useState, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
console.log("--------------test.js");

export class Test extends Component {

    static template = "test_template";


setup(){
console.log("--------------test.js");

onWillStart(async ()=>{
   console.log('-------------i am a component-------------');
   });
}


}
//registry.category("public_components").add("vendor_onboarding.test_dashboard", Test);
