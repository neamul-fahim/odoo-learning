# -*- coding: utf-8 -*-
# from odoo import http


# class SalesModulePortal(http.Controller):
#     @http.route('/sales_module_portal/sales_module_portal', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_module_portal/sales_module_portal/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_module_portal.listing', {
#             'root': '/sales_module_portal/sales_module_portal',
#             'objects': http.request.env['sales_module_portal.sales_module_portal'].search([]),
#         })

#     @http.route('/sales_module_portal/sales_module_portal/objects/<model("sales_module_portal.sales_module_portal"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_module_portal.object', {
#             'object': obj
#         })

