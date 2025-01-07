from odoo import http
from odoo.http import request

class ProjectList(http.Controller):
   @http.route('/projects/list', type='json', auth='public')
   def project_list(self):
      print(f"-------------------hello----------------")
      projects = request.env['project.project'].search([])
      project_data_list = []
      for project in projects:
         project_data = {
            'id': project.id,
            'name': project.name,
         }
         project_data_list.append(project_data)

      data_list = {
         'data': project_data_list
      }
      print(f"data_list ------------ {data_list['data']}")
      res = http.Response(template='dynamic_snippet.project_list',
                          qcontext=data_list)
      return res.render()
