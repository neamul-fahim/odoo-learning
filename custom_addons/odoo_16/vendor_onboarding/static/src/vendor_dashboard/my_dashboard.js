/** @odoo-module **/

import { Component, useRef, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { ProjectList } from './dashboard_item/dashboard_item';
import { Layout } from "@web/search/layout";

//import { jsonrpc } from "@web/core/network/rpc_service";



class MyAwesomeDashboard extends Component {
    static template = "my_awesome_dashboard.MyAwesomeDashboard";
    static components = { Layout, ProjectList };


   setup(){
   this.display = {
            controlPanel: {},
        };
   this.inputField = useRef('inputField');
   this.rpc = useService("rpc");
   this.user = useService("user");
   this.all_projects = useState({value:[]});
   this.projects = useService('my_awesome_dashboard.fetch_projects');

   onWillStart( async ()=>{
   try{
      this.all_projects.value = await this.projects.fetchProjects(this.user.userId);
       console.log(this.all_projects.value)

   }catch (error) {
            console.error("Error fetching projects:", error);
        }
   }
   );}






    async fetchProjects(inputValue){
        console.log('from fetchProjects------',inputValue)
        console.log('/my_awesome_dashboard/projects')

        try{
             this.all_projects.value = await this.projects.fetchProjects(inputValue);
//            const projects = await jsonrpc('/my_awesome_dashboard/projects', {inputValue: inputValue})

//            const projects = await this.rpc({
//            route: '/my_awesome_dashboard/projects',
//            params: {inputValue: inputValue}
//            });
            console.log("Projects fetched:", this.all_projects.value);
        }catch (error) {
                console.error("Error fetching projects:", error);
            }
    }
}

//registry.category("actions").add("my_awesome_dashboard.dashboard", MyAwesomeDashboard);
registry.category("public_components").add("vendor_dashboard", MyAwesomeDashboard);
