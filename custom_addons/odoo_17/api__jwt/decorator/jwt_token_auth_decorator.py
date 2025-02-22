import jwt
from odoo.http import request
from functools import wraps


SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"
EXPIRATION_TIME = 60 * 60


def jwt_token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Extract the JWT token from the Authorization header
        token = request.httprequest.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token[7:]  # Remove "Bearer " prefix
        print(f'jwt_token_required ----------- {token}')

        if not token:
            return {'error': 'Authorization token missing'}, 401

        try:
            # Decode the JWT token
            decoded = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

            # Find the user
            user_id = decoded.get('user_id')
            user = request.env['res.users'].sudo().browse(user_id)
            if not user:
                return {'error': 'User not found'}, 401

            # Set the current user in the request
            request.env.user = user

        except jwt.ExpiredSignatureError:
            return {'error': 'Token expired'}, 401
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}, 401

        return fn(*args, **kwargs)
    return wrapper