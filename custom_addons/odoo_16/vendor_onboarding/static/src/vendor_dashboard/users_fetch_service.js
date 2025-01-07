/** @odoo-module */
import { registry } from '@web/core/registry'


const usersFetchService = {
    dependencies: ['rpc'],
    start(env, {rpc}){
     return {
     async fetchUsers(){
    const users = await rpc('/users');
     return users;
    }
     }
    }
}


registry.category('services').add('my_awesome_dashboard.users', usersFetchService);