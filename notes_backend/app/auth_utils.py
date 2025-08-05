from datetime import datetime, timedelta
import jwt
from flask import current_app, request
from functools import wraps

# PUBLIC_INTERFACE
def generate_jwt(user_id, expires_in=86400):
    """
    Generate a JWT for the user.
    """
    secret = current_app.config["JWT_SECRET_KEY"]
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=expires_in)
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

# PUBLIC_INTERFACE
def decode_jwt(token):
    """
    Decodes a JWT, returns the payload if valid else raises.
    """
    secret = current_app.config["JWT_SECRET_KEY"]
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    return payload

# PUBLIC_INTERFACE
def login_required(fn):
    """
    Decorator to enforce JWT authentication on endpoints.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"message": "Missing or invalid authorization header"}, 401
        token = auth_header.replace("Bearer ", "")
        try:
            payload = decode_jwt(token)
            request.user_id = payload["user_id"]
        except Exception:
            return {"message": "Invalid or expired token"}, 401
        return fn(*args, **kwargs)
    return wrapper
