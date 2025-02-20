from datetime import datetime, timedelta, timezone
import jwt
from quart import request, jsonify
from functools import wraps
import os

# Secret key for JWT
SECRET_KEY = os.getenv('ADMIN_SESSION_SECRET', '')

# Generate JWT token
def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),  # 使用时区感知的 UTC 时间
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Decode and validate JWT token
def decode_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def login_required(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        token = request.cookies.get("auth_token")
        if not token:
            return jsonify({"error": "Unauthorized"}), 401

        user_data = decode_token(token)
        if not user_data:
            return jsonify({"error": "Invalid or expired token"}), 401

        # 将解码后的用户数据传递给实际的视图函数
        kwargs['user_data'] = user_data
        return await f(*args, **kwargs)
    return decorated_function 