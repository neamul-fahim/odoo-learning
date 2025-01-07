/** @odoo-module */

import { registry } from '@web/core/registry'
import { useState } from "@odoo/owl";
import { reactive } from "@odoo/owl";


const Count={
    start(env){
           const count = reactive({value:0});
           const increment = ()=>{
         count.value = count.value += 1;
        };
        const decrement= ()=>{
           count.value = count.value -= 1;
         };
      return{
        count,
        increment,
        decrement,
      }
    }
}

registry.category("services").add("global_or_shared_state.counter",Count);