from odoo import http, exceptions
from odoo.http import request
import jwt
import datetime
import logging
import json

SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"
EXPIRATION_TIME = 60 * 60 * 60

_logger = logging.getLogger(__name__)


def custom_authentication(username, password):
    try:
        uid = request.env['res.users'].authenticate(request.db, username, password, {})
        return uid
    except Exception as e:
        return None


class CustomLoginController(http.Controller):

    @http.route('/login_api', type='json', auth='none', csrf=False)
    def login_api(self, **post):
        if request.httprequest.method == 'POST':
            data = json.loads(request.httprequest.data)
            username = data.get('username')
            password = data.get('password')

            required_fields = ['username', 'password']
            # Check if all required fields are provided
            if not all(field in data for field in required_fields):
                return {'error': 'Missing required fields'}

            uid = custom_authentication(username, password)

            if uid:
                payload = {
                    'user_id': uid,
                    'username': username,
                    'exp': datetime.datetime.now() + datetime.timedelta(seconds=EXPIRATION_TIME),
                    'iat': datetime.datetime.now()
                }

                token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

                # Return JSON response with the token
                return {
                    'success': True,
                    'message': 'Login successful',
                    'token': token,
                }
            else:
                # Authentication failed, return JSON error message
                return {
                    'success': False,
                    'error': 'Invalid username or password. Please try again.'
                }

