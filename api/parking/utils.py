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
from api.parking.models import ParkingSession
from collections import Counter


def calculate_cost(check_out_time, check_in_time, price):
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
    cost = hours * price
    cost = round(cost, 1)

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


def generate_report(start_date, end_date):
    sessions = ParkingSession.query.filter(
        ParkingSession.check_in_time >= start_date,
        ParkingSession.check_in_time <= end_date
    ).all()

    total_sessions = len(sessions)
    total_earnings = round(sum(session.cost or 0 for session in sessions), 1)

    vip_sessions = sum(1 for session in sessions if session.spot.vip)
    regular_sessions = total_sessions - vip_sessions

    car_counts = Counter(session.car_license_plate for session in sessions)
    most_frequent_cars = [
        {"license_plate": plate, "sessions": count}
        for plate, count in car_counts.most_common(5)
    ]

    report = {
        "total_sessions": total_sessions,
        "total_earnings": total_earnings,
        "regular_sessions": regular_sessions,
        "vip_sessions": vip_sessions,
        "most_frequent_cars": most_frequent_cars,
    }

    return report