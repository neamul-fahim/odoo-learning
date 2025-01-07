/** @odoo-module */
import { Component, useRef, onWillStart, useState, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { ProjectList } from './dashboard_item/dashboard_item';
//import { Layout } from "@web/search/layout";

export class Test extends Component {
    static template = 'vendor_onboarding.test_template';
    static props = {};
    static components = { ProjectList };



   setup(){
   this.user = useService("vendor_onboarding.get_user");

   this.all_projects = useState({value:[]});
   this.projects = useService('vendor_onboarding.fetch_projects');

   onWillStart( async ()=>{
   try{
      const current_user = await this.user.fetchUser()
      console.log('user---------',current_user)
      this.all_projects.value = await this.projects.fetchProjects(current_user.id);
       console.log(this.all_projects.value)

   }catch (error) {
            console.error("Error fetching projects:", error);
        }
   }
   );
   };




}
registry.category("public_components").add("vendor_onboarding.test_dashboard", Test);
