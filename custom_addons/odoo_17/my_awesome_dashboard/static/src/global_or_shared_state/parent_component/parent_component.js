/** @odoo-module **/

import { Component, useRef, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { ChildComponent1 } from "../child_component_1/child_component_1"
import { ChildComponent2 } from "../child_component_2/child_component_2"

class ParentComponent extends Component {
static template = "my_awesome_dashboard.ParentComponent";
static components = {ChildComponent1,ChildComponent2}

}

registry.category("actions").add("my_awesome_dashboard.global_or_shared_state_owl_component",ParentComponent)