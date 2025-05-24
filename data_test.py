from api import db
from api.parking.models import Car, ParkingSpot, ParkingSession
from datetime import datetime, timedelta
import random
from app import create_app

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    cars = [
        Car(license_plate=f"AA{1000+i}BB", brand="Toyota", model=f"Model {i}", owner=f"Owner {i}")
        for i in range(12)
    ]
    db.session.add_all(cars)

    spots = [
        ParkingSpot(number=1, is_occupied=False, vip=False),
        ParkingSpot(number=2, is_occupied=False, vip=True),
        ParkingSpot(number=3, is_occupied=False, vip=False),
        ParkingSpot(number=4, is_occupied=False, vip=True),
        ParkingSpot(number=5, is_occupied=False, vip=False),
    ]
    db.session.add_all(spots)

    sessions = []
    for i in range(5):
        car = random.choice(cars)
        spot = random.choice(spots)
        check_in = datetime.now() - timedelta(hours=random.randint(1, 5))
        check_out = check_in + timedelta(hours=random.randint(1, 3))
        cost = round(random.uniform(10, 50), 2)

        session = ParkingSession(
            car_license_plate=car.license_plate,
            spot_number=spot.number,
            check_in_time=check_in,
            check_out_time=check_out,
            cost=cost
        )
        sessions.append(session)

    db.session.add_all(sessions)

    db.session.commit()

    print("✅ Тестові дані успішно додано!")
