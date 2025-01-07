from odoo import http
from odoo.http import request
import logging
import json

_logger = logging.getLogger(__name__)

class SignupController(http.Controller):

    @http.route('/signup_api', type='json', auth='public', methods=['POST'], csrf=False)
    def signup(self, **kwargs):
        data = json.loads(request.httprequest.data)

        required_fields = ['name', 'email', 'password']

        # Check if all required fields are provided
        if not all(field in data for field in required_fields):
            return {'error': 'Missing required fields'}

        # Check if email is already used
        existing_user = request.env['res.users'].sudo().search([('login', '=', data.get('email'))])
        if existing_user:
            return {'error': 'Email already registered'}

        # Create a new user
        try:
            user = request.env['res.users'].sudo().create({
                'name': data.get('name'),
                'login': data.get('email'),
                'email': data.get('email'),
                'password': data.get('password'),
            })
            return {'message': 'User created successfully', 'user_id': user.id}
        except Exception as e:
            _logger.error(f"An error occurred while creating the user: {str(e)}")
            return {'error': 'An error occurred while creating the user'}
