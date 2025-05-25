import uuid

from flask import session

from api.auth.models import User
from api.utils.errors import ContentNotFoundError
from utils.constants import OBJECT_NOT_FOUND, STATUS_NOT_FOUND


def get_user_by_id(id):
    """
    Retrieves an user from the database by its id.

    Args:
        id (str): The id of the user.

    Returns:
        Any: The retrieved object or None if not found.
    """
    obj = User.query.filter_by(id=id).first()
    if not obj:
        raise ContentNotFoundError(
            OBJECT_NOT_FOUND.format(User.__name__), status_code=STATUS_NOT_FOUND
        )

    return obj


def get_session_id():
    """
    Retrieves the session ID from the request context.

    Returns:
        str: The session ID.
    """
    session_id = session.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        session["session_id"] = session_id

    return session_id
