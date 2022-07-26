from flask import request, jsonify, current_app as app
from functools import wraps
import datetime
from werkzeug.security import check_password_hash
import jwt

from app.exceptions.auth_error import AuthError
from app.repository.users import get_by_login

def auth():
    auth = request.authorization
    validate_auth(auth)
    user = get_by_login(auth.username)
    if not (user and check_password_hash(user.password, auth.password)):
        raise AuthError({
            'code': 'not_found',
            'description': 'User not found'
        }, 401)

    exp = datetime.datetime.now() + datetime.timedelta(hours=12)
    token = jwt.encode(payload={
        'login': user.login,
        'exp': exp
    }, key=app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        'type': 'Bearer',
        'token': token,
        'exp': exp,
    })

def validate_auth(auth):
    if not (auth and auth.username and auth.password):
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected'
            }, 401)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization').replace('Bearer ', '')
        if not token:
            raise AuthError({
                'code': 'auth_token_missing',
                'description': 'Token is missing from request'
            }, 401)

        try:
            data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = get_by_login(data)
            return f(current_user, *args, **kwargs)
        except Exception as inst:
            raise AuthError({
                'code': 'auth_token_invalid',
                'description': 'Token is invalid or expired',
                'debug': inst.args
            }, 401)
    return decorated
