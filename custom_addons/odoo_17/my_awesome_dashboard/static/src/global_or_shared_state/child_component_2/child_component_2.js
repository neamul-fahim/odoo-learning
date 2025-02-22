/** @odoo-module **/

import { Component, useRef, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";

export class ChildComponent2 extends Component {
static template = "my_awesome_dashboard.ChildComponent2";
setup(){
  this.count_obj = useState(useService("global_or_shared_state.counter"));
}



increment(){
this.count_obj.increment();
}
decrement(){
this.count_obj.decrement();

}
}
