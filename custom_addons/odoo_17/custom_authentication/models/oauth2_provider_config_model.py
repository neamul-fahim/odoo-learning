from odoo import models, fields

class OAuth2ProviderConfig(models.Model):
    _name = 'auth.oauth2.provider'
    _description = 'OAuth2 Provider Configuration'

    name = fields.Char('Provider Name', required=True)
    client_id = fields.Char('Client ID', required=True)
    client_secret = fields.Char('Client Secret', required=True)
    auth_endpoint = fields.Char('Authorization Endpoint', required=True)
    token_endpoint = fields.Char('Token Endpoint', required=True)
    userinfo_endpoint = fields.Char('User Info Endpoint', required=True)
