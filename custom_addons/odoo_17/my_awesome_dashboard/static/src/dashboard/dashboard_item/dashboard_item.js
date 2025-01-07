/** @odoo-module **/

import { Component } from "@odoo/owl";
import { ProjectCard } from '../project_card/project_card';


export class ProjectList extends Component {
    static template = "my_awesome_dashboard.ProjectList";
    static components = { ProjectCard };

 static props = {
        all_projects: Array,  // The 'projects' prop must be an array of project objects
    };

//    setup() {
//        // The parent will pass 'all_projects' as props
//        this.projects = this.props.all_projects;
//    }
}
