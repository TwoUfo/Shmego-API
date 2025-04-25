import pytest
from flask import Flask
from app import db
from utils.constants import *
from api import blueprint
 
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "test_secret_key"
 
    db.init_app(app)
    app.register_blueprint(blueprint)
 
    with app.app_context():
        db.create_all()
 
    yield app
 
    with app.app_context():
        db.session.remove()
        db.drop_all()
 
@pytest.fixture
def client(app):
    return app.test_client()
 
 
def test_add_car(client):
    response = client.post("/api/parking/cars", json={
        KEY_LICENSE_PLATE: "AA1234BB",
        KEY_BRAND: "Toyota",
        KEY_MODEL: "Corolla",
        KEY_OWNER: "John Doe"
    })
    assert response.status_code == 201
    assert response.json["message"] == MSG_CAR_ADDED
 
 
def test_get_car(client):
    test_add_car(client)
    response = client.get("/api/parking/cars/AA1234BB")
    assert response.status_code == 200
    assert response.json["data"][KEY_OWNER] == "John Doe"
 
 
def test_add_spot(client):
    response = client.post("/api/parking/spots", json={
        KEY_NUMBER: 0,
        KEY_IS_OCCUPIED: False
    })
    assert response.status_code == 201
    assert response.json["message"] == MSG_SPOT_ADDED
 
 
def test_check_in(client):
    test_add_car(client)
    test_add_spot(client)
    response = client.post("/api/parking/sessions/check-in", json={
        KEY_CAR_LICENSE_PLATE: "AA1234BB",
        KEY_SPOT_NUMBER: 0,
    })
    assert response.status_code == 201
    assert response.json["message"] == MSG_SESSION_STARTED
    assert KEY_SESSION_ID in response.json["data"]
 
 
def test_check_out(client):
    test_check_in(client)
    response = client.post("/api/parking/sessions/check-out/AA1234BB")
    assert response.status_code == 200
    assert response.json["message"] == MSG_CHECKED_OUT_SUCCESS
    assert KEY_COST in response.json["data"]
    assert KEY_DURATION_HOURS in response.json["data"]
 
 
def test_check_in_on_occupied_spot(client):
    test_check_in(client)
    response = client.post("/api/parking/sessions/check-in", json={
        KEY_CAR_LICENSE_PLATE: "AA1234BB",
        KEY_SPOT_NUMBER: 0,
    })
    assert response.status_code == 400
 
 
def test_add_duplicate_car(client):
    test_add_car(client)
    response = client.post("/api/parking/cars", json={
        KEY_LICENSE_PLATE: "AA1234BB",
        KEY_BRAND: "Toyota",
        KEY_MODEL: "Corolla",
        KEY_OWNER: "John Doe"
    })
    assert response.status_code == 400
    assert response.json["message"] == ERR_CAR_EXISTS
 
 
def test_check_in_nonexistent_car(client):
    test_add_spot(client)
    response = client.post("/api/parking/sessions/check-in", json={
        KEY_CAR_LICENSE_PLATE: "ZZ9999ZZ",
        KEY_SPOT_NUMBER: 0,
    })
    assert response.status_code == 404
    assert response.json["message"] == ERR_OBJECT_NOT_FOUND.format(KEY_CAR.format("ZZ9999ZZ"))
 
 
def test_check_in_nonexistent_car_and_spot(client):
    test_add_spot(client)
    response = client.post("/api/parking/sessions/check-in", json={
        KEY_CAR_LICENSE_PLATE: "ZZ9999ZZ",
        KEY_SPOT_NUMBER: 99,
    })
    assert response.status_code == 404
 
 
def test_check_in_nonexistent_spot(client):
    test_add_car(client)
    response = client.post("/api/parking/sessions/check-in", json={
        KEY_CAR_LICENSE_PLATE: "AA1234BB",
        KEY_SPOT_NUMBER: 99,
    })
    assert response.status_code == 404
    assert response.json["message"] == ERR_OBJECT_NOT_FOUND.format(KEY_SPOT.format(99))
 
 
def test_check_out_car_not_in_session(client):
    test_add_car(client)
    response = client.post("/api/parking/sessions/check-out/AA1234BB")
    assert response.status_code == 404
    assert response.json["message"] == ERR_OBJECT_NOT_FOUND.format(KEY_SESSION.format("AA1234BB"))
 
 
def test_update_car(client):
    test_add_car(client)
 
    response = client.put("/api/parking/cars/AA1234BB", json={
        KEY_LICENSE_PLATE: "AA1234BB",
        KEY_BRAND: "Honda",
        KEY_MODEL: "Civic",
        KEY_OWNER: "Jane Doe"
    })
    assert response.status_code == 200
    assert response.json["message"] == MSG_CAR_UPDATED
 
    response = client.get("/api/parking/cars/AA1234BB")
    assert response.status_code == 200
    assert response.json["data"][KEY_BRAND] == "Honda"
    assert response.json["data"][KEY_MODEL] == "Civic"
    assert response.json["data"][KEY_OWNER] == "Jane Doe"
 
 
def test_update_spot(client):
    test_add_spot(client)
 
    response = client.put("/api/parking/spots/0", json={
        KEY_NUMBER: 0,
        KEY_IS_OCCUPIED: True
    })
    assert response.status_code == 200
    assert response.json["message"] == MSG_SPOT_UPDATED
 
    response = client.get("/api/parking/spots/0")
    assert response.status_code == 200
    assert response.json["data"][KEY_IS_OCCUPIED] is True
 
 
def test_update_nonexistent_car(client):
    response = client.put("/api/parking/cars/ZZ9999ZZ", json={
        KEY_LICENSE_PLATE: "ZZ9999ZZ",
        KEY_BRAND: "Mazda",
        KEY_MODEL: "3",
        KEY_OWNER: "Ghost"
    })
    assert response.status_code == 404
 
 
def test_update_nonexistent_spot(client):
    response = client.put("/api/parking/spots/99", json={
        KEY_NUMBER: 99,
        KEY_IS_OCCUPIED: True
    })
    assert response.status_code == 404
 
def test_update_car_1(client):
    test_add_car(client)
    response = client.put("/api/parking/cars/AA1234BB", json={
        KEY_LICENSE_PLATE: "AA1234BB",
        KEY_BRAND: "Honda",
        KEY_MODEL: "Civic",
        KEY_OWNER: "Jane Doe"
    })
    assert response.status_code == 200
    assert response.json["message"] == MSG_CAR_UPDATED
 
    updated = client.get("/api/parking/cars/AA1234BB")
    assert updated.status_code == 200
    assert updated.json["data"][KEY_OWNER] == "Jane Doe"
 
 
def test_update_spot_1(client):
    test_add_spot(client)
    response = client.put("/api/parking/spots/0", json={
        KEY_NUMBER: 0,
        KEY_IS_OCCUPIED: True
    })
    assert response.status_code == 200
    assert response.json["message"] == MSG_SPOT_UPDATED
 
    # Перевірка оновлення
    updated = client.get("/api/parking/spots/0")
    assert updated.status_code == 200
    assert updated.json["data"][KEY_IS_OCCUPIED] is True
 
 
def test_get_all_cars(client):
    test_add_car(client)
    response = client.get("/api/parking/cars")
    assert response.status_code == 200
    assert isinstance(response.json["data"], list)
    assert len(response.json["data"]) >= 1
 
 
def test_get_all_spots(client):
    test_add_spot(client)
    response = client.get("/api/parking/spots")
    assert response.status_code == 200
    assert isinstance(response.json["data"], list)
    assert len(response.json["data"]) >= 1
 
 
def test_get_sessions(client):
    test_check_in(client)
    response = client.get("/api/parking/sessions")
    assert response.status_code == 200
    assert isinstance(response.json["data"], list)
    assert len(response.json["data"]) >= 1