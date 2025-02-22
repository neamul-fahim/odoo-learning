/** @odoo-module */
import { registry } from '@web/core/registry'


const GetUserService = {
    dependencies: ['rpc'],
    start(env, {rpc}){
     return {
     async fetchUser(){
    const user = await rpc('/vendor_onboarding/get_user');
     return user;
    }
     }
    }
}


registry.category('services').add('vendor_onboarding.get_user', GetUserService);