# controllers.py
from odoo import http
from odoo.http import request

class OwlBasicApp(http.Controller):
    @http.route(['/basic_owl'], type='http', auth='public', website='True')
    def basic_owl_page(self):
        print(f'hello world')
        """
        Render the basic Owl page
        """
        return request.render('owl_framework_practice.basic_owl_template',
                              {
                                  'session_info': request.env['ir.http'].get_frontend_session_info(),
                              }
                              )
