from functools import wraps
from models.user import User
from utils.utils import get_response
from flask_jwt_extended import jwt_required, get_jwt_identity

def login_required():
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            username = get_jwt_identity()

            user = User.query.filter_by(username=username).first()
            if not user:
                return get_response("User not found", None, 404), 404
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
