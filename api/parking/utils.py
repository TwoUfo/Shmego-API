from api import db
from api.parking.errors import (
    ObjectNotFound,
    SessionAlreadyCheckedOut,
    SpotAlreadyOccupied,
)
from utils.constants import (
    ERR_OBJECT_NOT_FOUND,
    ERR_SPOT_OCCUPIED,
    MSG_ALREADY_CHECKED_OUT,
)


def calculate_cost(check_out_time, check_in_time):
    """
    Calculate the parking cost based on the check-in and check-out times.
    The cost is calculated at a rate of 25 UAH per hour, with a minimum charge of 1 hour.

    Args:
        check_out_time (datetime): The time the car was checked out.
        check_in_time (datetime): The time the car was checked in.

    Returns:
        tuple: A tuple containing the cost and the duration in hours.
    """
    duration = check_out_time - check_in_time
    hours = max(1, int(duration.total_seconds() // 3600))
    cost = hours * 25

    return cost, hours


def check_session_status(session):
    if session.check_out_time is not None:
        raise SessionAlreadyCheckedOut(MSG_ALREADY_CHECKED_OUT, 400)


def check_object_exists(obj, type_name):
    if obj is None:
        raise ObjectNotFound(ERR_OBJECT_NOT_FOUND, type_name, 404)


def check_is_spot_occupied(spot):
    if spot.is_occupied:
        raise SpotAlreadyOccupied(ERR_SPOT_OCCUPIED, 400)
