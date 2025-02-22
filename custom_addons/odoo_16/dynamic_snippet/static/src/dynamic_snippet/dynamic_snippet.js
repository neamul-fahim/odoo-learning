

odoo.define('dynamic_snippet_blog.dynamic', function (require) {
   var PublicWidget = require('web.public.widget');
   var rpc = require('web.rpc');
   var Dynamic = PublicWidget.Widget.extend({
       selector: '.dynamic_snippet',
       start: function () {
           console.log('----------------javascript------------------')

           var self = this;
           rpc.query({
               route: '/projects/list',
               params: {},
           }).then(function (result) {
               self.$target.empty().append(result);
           });
       },
   });
   PublicWidget.registry.dynamic_snippet_blog = Dynamic;
   return Dynamic;
});





///** @odoo-module **/
//
//import publicWidget from "@web/legacy/js/public/public_widget";
//import { jsonrpc } from "@web/core/network/rpc_service";
//
//publicWidget.registry.DynamicSnippet = publicWidget.Widget.extend({
//   selector: '.dynamic_snippet',
//   start: function () {
//       console.log('----------------javascript------------------')
//       var self = this;
//       var data = jsonrpc('/projects/list', {}).then((data) => {
//           self.$target.empty().append(data)
//       });
//       console.log('projects data',data)
//   }
//});
//
//export default publicWidget.registry.DynamicSnippet;