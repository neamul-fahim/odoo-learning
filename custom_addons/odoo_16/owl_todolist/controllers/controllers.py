# -*- coding: utf-8 -*-
# from odoo import http


# class OwlTodolist(http.Controller):
#     @http.route('/owl_todolist/owl_todolist', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/owl_todolist/owl_todolist/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('owl_todolist.listing', {
#             'root': '/owl_todolist/owl_todolist',
#             'objects': http.request.env['owl_todolist.owl_todolist'].search([]),
#         })

#     @http.route('/owl_todolist/owl_todolist/objects/<model("owl_todolist.owl_todolist"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('owl_todolist.object', {
#             'object': obj
#         })
