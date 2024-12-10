from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def authorize(required_roles=None):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()

                user_role = claims.get('role')
                if required_roles and user_role not in required_roles:
                    return jsonify({'message': 'Access denied: insufficient permissions'}), 403

            except Exception as e:
                return jsonify({'message': 'Unauthorized', 'error': str(e)}), 401

            return f(*args, **kwargs)
        return decorator
    return wrapper
