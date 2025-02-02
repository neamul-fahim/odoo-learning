import requests
from odoo import http
from odoo.http import request
from werkzeug.utils import redirect



class OAuth2Controller(http.Controller):

    @http.route('/auth_oauth2/login', auth='public', type='http')
    def oauth2_login(self):
        provider = request.env['auth.oauth2.provider'].search([], limit=1)
        if not provider:
            return "OAuth2 provider not configured"

        redirect_uri = request.httprequest.host_url + 'custom_auth/google/callback'
        auth_url = f"{provider.auth_endpoint}?client_id={provider.client_id}&redirect_uri={redirect_uri}&response_type=code&scope=email%20profile&access_type=offline"
        print(f'URL ========================== {auth_url}')
        return redirect(auth_url)

    @http.route('/custom_auth/google/callback/', auth='public', type='http')
    def oauth2_callback(self, **kwargs):
        code = kwargs.get('code')
        provider = request.env['auth.oauth2.provider'].search([], limit=1)
        redirect_uri = request.httprequest.host_url + 'custom_auth/google/callback'

        if not code:
            return "No authorization code provided"

        # Exchange code for access token
        token_data = {
            'code': code,
            'client_id': provider.client_id,
            'client_secret': provider.client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }

        response = requests.post(provider.token_endpoint, data=token_data)
        response_data = response.json()

        if 'access_token' not in response_data:
            return "Failed to obtain access token"

        access_token = response_data['access_token']
        user_info_response = requests.get(provider.userinfo_endpoint,
                                          headers={'Authorization': f'Bearer {access_token}'})
        user_info = user_info_response.json()
        print(f'user email =========================== {user_info}')
        # # Handle user login or creation
        # user = request.env['res.users'].sudo().search([('login', '=', user_info['email'])], limit=1)
        #
        # if not user:
        #     user = request.env['res.users'].sudo().create({
        #         'name': user_info['name'],
        #         'login': user_info['email'],
        #         'email': user_info['email'],
        #     })
        #
        # request.env.cr.commit()
        # request.session.authenticate(request.session.db, user.login, '')
        #
        # return request.redirect('/web')
