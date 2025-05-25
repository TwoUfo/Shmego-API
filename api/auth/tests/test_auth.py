import pytest
from flask import Flask, session
from app import db
from api import blueprint
from api.auth.models import User  # або звідки імпортується твоя модель User
from utils.constants import *
from api.utils.auth_handler import (
    generate_jwt,
    decode_jwt,
)


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "test-secret"
    app.config["SESSION_TYPE"] = "filesystem"

    db.init_app(app)
    app.register_blueprint(blueprint)

    with app.app_context():
        db.create_all()
        # Додай тестового користувача
        user = User(id="testuser1", role="op")
        db.session.add(user)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_login_success(client):
    response = client.post("/api/auth/login", json={
        "id": "testuser1"
    })

    assert response.status_code == 200
    assert response.json["message"] == LOGIN_SUCCESS
    assert ACCESS_TOKEN in response.headers.get("Set-Cookie", "")


def test_login_not_found(client):
    response = client.post("/api/auth/login", json={
        "id": "invaliduser"
    })

    assert response.status_code == STATUS_NOT_FOUND
    assert response.json["message"] == "User not found"


def test_logout_success(client):
    # Спочатку увійти
    login_resp = client.post("/api/auth/login", json={
        "id": "testuser1"
    })

    assert login_resp.status_code == 200
    cookie = login_resp.headers.get("Set-Cookie")

    # Вийти, передавши токен через cookie
    response = client.post(
        "/api/auth/logout",
        headers={"Cookie": cookie}
    )

    assert response.status_code == 200
    assert response.json["message"] == LOG_OUT_SUCCESS


def test_logout_unauthorized(client):
    response = client.post("/api/auth/logout")
    assert response.status_code == STATUS_UNAUTHORIZED
    assert response.json["message"] == SESSION_EXPIRED


def test_generate_and_decode_jwt():
    session_id = "abc123"
    token = generate_jwt(session_id, expires_in=10)

    decoded = decode_jwt(token)

    assert decoded is not None
    assert decoded["session_id"] == session_id


