/** @odoo-module **/

import { Component, useRef, onWillStart, useState, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class Test extends Component {
    static template = xml`<div>---------XML of a Component---------</div>`;


setup(){
onWillStart(async ()=>{
   console.log('-------------i am a component-------------');
   });
}


}
registry.category("public_components").add("test_dashboard", Test);
