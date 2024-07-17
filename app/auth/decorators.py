# app/auth/decorators.py

from functools import wraps
from flask import request, jsonify
from app.models import User
from app import app


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        user = User.query.filter_by(token=token).first()

        if not user:
            return jsonify({'error': 'Invalid token'}), 401

        request.user = user
        return f(*args, **kwargs)
    return decorated_function

def admin_api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')

        if not api_key or api_key != app.config['ADMIN_API_KEY']:
            return jsonify({'error': 'Unauthorized access'}), 401

        return f(*args, **kwargs)
    return decorated_function