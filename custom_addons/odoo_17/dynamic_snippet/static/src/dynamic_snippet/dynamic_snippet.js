/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.DynamicSnippet = publicWidget.Widget.extend({
   selector: '.dynamic_snippet',
   start: function () {
       console.log('----------------javascript------------------')
       var self = this;
       var data = jsonrpc('/projects/list', {}).then((data) => {
           self.$target.empty().append(data)
       });
       console.log('projects data',data)
   }
});

export default publicWidget.registry.DynamicSnippet;