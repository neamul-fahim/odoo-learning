from odoo import http, exceptions
from odoo.http import request
from werkzeug.wrappers import Response
from werkzeug.utils import redirect
import jwt
import datetime
from ..decorators import jwt_required
from werkzeug.security import check_password_hash

# from custom_addons.odoo_17.vendor_onboarding.decorators.jwt_token_auth_decorator import jwt_required

SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"
EXPIRATION_TIME = 60 * 60

class CustomLoginController(http.Controller):

    @http.route('/user_login', type='http', auth='public', website=True, csrf=False)
    def user_login(self, **post):
        if request.httprequest.method == 'POST':
            username = post.get('username')
            password = post.get('password')
            print(f'username------ {username}  password-------- {password}')

            uid = self.custom_authentication(username,password)
            print(f'uid-----------{uid}')


            if uid:
                payload = {
                    'user_id': uid,
                    'username': username,
                    'exp': datetime.datetime.now() + datetime.timedelta(seconds=EXPIRATION_TIME),
                    'iat': datetime.datetime.now()
                }

                token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
                print(f"token----------------------{token}")

                # Step 4: Return the token
                response = redirect('/my_home')
                response.set_cookie('Authorization', token, httponly=True, samesite='Strict')

                return response


            else:
                # Authentication failed, render the page with an error message
                return request.render('vendor_onboarding.custom_login_page', {
                    'error': 'Invalid username or password. Please try again.'
                })

        print(f'Default behavior for GET requests')
        # Default behavior for GET requests (if someone accesses /user_login via a browser directly)
        return request.render('vendor_onboarding.custom_login_page', {})


    @http.route('/my_home', type='http', auth='none', website=True, csrf=False)
    @jwt_required
    def my_home(self):
        print(f'controller user id ----------- {request.env.user}')
        return Response("Login Successful")



    def custom_authentication(self, username, password):
        try:
            uid = request.env['res.users'].authenticate(request.db, username, password, {})
            return uid
        except Exception as e:
            return None


    # def custom_authentication(self, username, password):
    #     user = request.env['res.users'].sudo().search([('login', '=', username)], limit=1)
    #     print(f'user id(_check_credentials) ------------------ {user.id} ----- ')
    #
    #     request.env.cr.execute(
    #         "SELECT COALESCE(password, '') FROM res_users WHERE id=%s",
    #         [int(user.id)]
    #     )
    #     print(f'ans  ------- {ans}')
    #
    #     [hashed] = request.env.cr.fetchone()
    #     valid, replacement = request._crypt_context() \
    #         .verify_and_update(password, hashed)
    #     print(f'result------------{valid}')
    #
    #     if user:
    #         # Use Werkzeug's helper method to validate a password with the hash stored in user.password_crypt (hashed field in Odoo user record)
    #         if check_password_hash(user.password, password):
    #             return user.id
    #
    #     return None
    #
    #     # user_agent_env = {
    #     #     'HTTP_USER_AGENT': request.httprequest.headers.get('User-Agent', ''),
    #     #     'REMOTE_ADDR': request.httprequest.remote_addr,
    #     #     'interactive': True,  # Non-interactive scenario, like API usage
    #     # }
    #
    #     user_agent_env = {
    #         'interactive': True,
    #         # 'base_location': request.httprequest.url_root.rstrip('/'),
    #         'HTTP_HOST': request.httprequest.environ['HTTP_HOST'],
    #         'REMOTE_ADDR': request.httprequest.environ['REMOTE_ADDR'],
    #     }
    #
    #     if user and user._check_credentials(password, user_agent_env):
    #         return user.id
    #     else:
    #         return None