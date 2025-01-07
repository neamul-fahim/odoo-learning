from odoo import http
from odoo.http import request

class ProjectController(http.Controller):
    @http.route('/my_awesome_dashboard/projects', type='json', auth='public', csrf=False, website=True)
    def get_projects(self, **kw):
        print(f'----------------------------- controller-----------------------------')
        query_param= kw.get('inputValue')
        print(f'query_param------------------ {query_param}')

        domain = []
        domain.append(('user_id', '=', int(query_param)))
        projects = request.env['project.project'].search(domain)
        return [{'id': project.id, 'name': project.name} for project in projects]

    @http.route('/users', type='json', auth='user', csrf=False)
    def get_users(self):
        users = request.env['res.users'].search([])
        return [{'id': user.id, 'name': user.name} for user in users]