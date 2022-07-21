from flask import request, jsonify, current_app as app
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
        })

    exp = datetime.datetime.now() + datetime.timedelta(hours=12)
    token = jwt.encode(payload={
        'login': user.login,
        'exp': exp
    }, key=app.config['SECRET_KEY'])

    return jsonify({
        'token': token,
        'exp': exp,
    })

def validate_auth(auth):
    if not (auth and auth.username and auth.password):
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected'
            }, 401)
