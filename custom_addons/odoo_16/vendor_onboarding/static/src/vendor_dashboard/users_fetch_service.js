/** @odoo-module */
import { registry } from '@web/core/registry'

console.log("--------------users_fetch_service.js");

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