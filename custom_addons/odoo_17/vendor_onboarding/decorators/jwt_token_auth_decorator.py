import functools
import jwt
from werkzeug.wrappers import Response
from odoo.http import request

SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"

def jwt_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Fetch the token from cookie
        token = request.httprequest.cookies.get('Authorization')
        print(f'decorator token -----------{token}')
        if not token:
            return Response('Missing token', status=401)

        try:
            # Decode the token to get the user ID
            data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            user_id = data.get('user_id')
            print(f'decorator user_id----------------- {user_id}')
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return Response('Invalid token', status=403)
        request.env.user = user_id

        return func(*args, **kwargs)

    return wrapper