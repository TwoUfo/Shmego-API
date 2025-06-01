from flask import request, session
from flask_restx import Resource

from api.auth import ns
from api.auth.schemas import get_userid_model
from api.auth.utils import get_session_id, get_user_by_id
from api.utils.auth_handler import (
    decode_jwt,
    generate_jwt,
    login_required,
    set_cookie,
)
from api.utils.errors import ContentNotFoundError
from api.utils.response import response
from utils.constants import *


@ns.route("/login")
class Login(Resource):
    """
    Handles user authentication and session management.
    """

    @ns.expect(get_userid_model(ns))
    def post(self):
        """
        Authenticates a user and starts a session.

        Returns:
            - 200 OK: If the login is successful. Sets a secure HTTP-only cookie with the access token.
            - 400 Bad Request: If the credentials are invalid or missing.
            - 404 Not Found: If the user with the given email does not exist.
        """
        try:
            data = request.get_json()
            user_id = data.get("id")

            user = get_user_by_id(user_id)

            session[KEY_USER_ID] = user.id
            session[KEY_ROLE] = user.role

            session_id = get_session_id()

            access_token = generate_jwt(session_id, user.role, expires_in=EIGHT_HOURS)

            resp = response(
                message=LOGIN_SUCCESS, data={"role": user.role}, status_code=STATUS_OK
            )
            resp = set_cookie(resp, ACCESS_TOKEN, access_token)

            return resp
        except ContentNotFoundError as e:
            return response(message=e.args[0], status_code=STATUS_NOT_FOUND)
        except ValueError as e:
            return response(
                message=LOGIN_FAILED_INVALID_CREDENTIALS, status_code=STATUS_BAD_REQUEST
            )
        except Exception as e:
            return response(message=LOGIN_FAILED, status_code=STATUS_BAD_REQUEST)


@ns.route("/logout")
class Logout(Resource):
    """
    Handles user logout and session termination.
    """

    @login_required
    def post(self):
        """
        Logs out the currently authenticated user.

        Clears the session and removes the access token cookie.

        Returns:
            - 200 OK: If logout is successful.
            - 401 Unauthorized: If the user is not authenticated.
            - 400 Bad Request: If an unexpected error occurs during logout.
        """
        try:
            session.clear()

            resp = response(message=LOG_OUT_SUCCESS, status_code=STATUS_OK)
            resp.delete_cookie(ACCESS_TOKEN)

            return resp
        except Exception as e:
            return response(message=LOGOUT_FAILED, status_code=STATUS_BAD_REQUEST)
