/** @odoo-module */
import { registry } from '@web/core/registry'


const projectsFetchService = {
    dependencies: ['rpc'],
    start(env, {rpc}){
     return {
     async fetchProjects(inputValue){
    const projects = await rpc('/my_awesome_dashboard/projects', {inputValue: inputValue});
     return projects;
    }
     }
    }
}


registry.category('services').add('my_awesome_dashboard.fetch_projects', projectsFetchService);