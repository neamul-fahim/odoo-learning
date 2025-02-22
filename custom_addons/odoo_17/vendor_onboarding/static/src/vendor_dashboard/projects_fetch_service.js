/** @odoo-module */
import { registry } from '@web/core/registry'


const projectsFetchServiceVendor = {
    dependencies: ['rpc'],
    start(env, {rpc}){
     return {
     async fetchProjects(inputValue){
     console.log('user id ---------------------- ',inputValue);
    const projects = await rpc('/vendor_onboarding/projects', {inputValue: inputValue});
     return projects;
    }
     }
    }
}


registry.category('services').add('vendor_onboarding.fetch_projects', projectsFetchServiceVendor);