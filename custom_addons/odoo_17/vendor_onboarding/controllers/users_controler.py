from odoo import http
from odoo.http import request

class VendorProjectController(http.Controller):
    @http.route('/vendor_onboarding/projects', type='json', auth='public', csrf=False, website=True)
    def get_vendor_projects(self, **kw):
        print(f'----------------------------- controller-----------------------------')
        query_param= kw.get('inputValue')
        print(f'query_param------------------ {query_param}')

        domain = []
        domain.append(('portal_user_ids', '=', int(query_param)))
        projects = request.env['project.task'].sudo().search(domain)
        print(f'projects---------- {len(projects)}')
        state_mapping = dict(request.env['project.task'].fields_get(['state'])['state']['selection'])

        project_data = []
        for project in projects:
            project_data.append({
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'date_deadline': project.date_deadline,
                'state': state_mapping.get(project.state, 'Unknown'),  # Get the plain text label for the state
            })
        return project_data

    @http.route('/vendor_onboarding/get_user', type='json', auth='user', csrf=False)
    def get_current_user(self):
        current_user = request.env.user
        print(f'got user------{current_user.id}')
        return {
            'id': current_user.id,
            'name': current_user.name,
        }