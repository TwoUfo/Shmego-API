import datetime
import os
from functools import wraps
from typing import Any, Callable, Optional

import jwt
from flask import Response, request, session

from api.utils.response import response
from utils.constants import *

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


def set_cookie(response: Response, key: str, value: str) -> Response:
    """
    Set a cookie in the response.

    Args:
        response (Response): The Flask response object.
        key (str): The name of the cookie.
        value (str): The value of the cookie.

    Returns:
        Response: The updated response object with the cookie set.
    """
    response.set_cookie(
        key, value, httponly=True, samesite="Strict", secure=False, max_age=None
    )
    return response


def generate_jwt(session_id: str, expires_in: int = 28800) -> str:
    """
    Generates a JWT token with a session ID and an expiration time.

    Args:
        session_id (str): The session ID to include in the JWT payload.

    Returns:
        str: The generated JWT token.
    """
    payload = {
        "session_id": session_id,
        "exp": datetime.datetime.now() + datetime.timedelta(seconds=expires_in),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ENCODE_ALGORITHM)


def decode_jwt(token: str) -> Optional[dict[str, Any]]:
    """
    Decodes the JWT token and returns the payload.

    Args:
        token (str): The JWT token to be decoded.

    Returns:
        dict | None: The decoded payload if the token is valid, otherwise None.
    """
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ENCODE_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def login_required(fn: Callable) -> Callable:
    """
    Decorator that checks if the user is logged in by verifying the presence of a valid JWT token.

    Args:
        fn (function): The function to be wrapped.

    Returns:
        function: The wrapped function that checks if the user is logged in before executing.
    """

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        token: Optional[str] = request.cookies.get("access_token")
        print(token)
        
        payload = decode_jwt(token)
        print(payload)
        if not payload:
            
            return response(message=SESSION_EXPIRED, status_code=STATUS_UNAUTHORIZED)

        if not token:
            return response(message=TOKEN_IS_MISSING, status_code=STATUS_UNAUTHORIZED)

        session_id: Optional[str] = payload.get("session_id")
        if not session_id:
            return response(
                message=SESSION_ID_IS_MISSING, status_code=STATUS_UNAUTHORIZED
            )

        if not session.get("id"):
            return response(message=SESSION_EXPIRED, status_code=STATUS_UNAUTHORIZED)

        return fn(*args, **kwargs)

    return wrapper


def admin_required(fn: Callable) -> Callable:
    """
    Decorator that checks if the user is an admin, in addition to being logged in.

    Args:
        fn (function): The function to be wrapped.

    Returns:
        function: The wrapped function that checks if the user is an admin before executing.
    """

    @wraps(fn)
    @login_required
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        role = session.get("role")
        if role != "admin":
            return response(message=REQUEST_DENIED, status_code=STATUS_FORBIDDEN)
        return fn(*args, **kwargs)

    return wrapper
