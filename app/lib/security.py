from exceptions.auth_error import AuthError

def validate_token(auth):
    if not auth:
        raise AuthError({
            "code": "authorization_header_missing",
            "description": "Authorization header is expected"
            }, 401)

    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must be Bearer token"
            }, 401)
