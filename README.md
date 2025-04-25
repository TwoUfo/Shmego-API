# Shmego-API

This project is a Flask REST API for managing a parking system, which allows you to:
- Add, update, and retrieve information about cars
- Create and manage parking spots
- Track parking sessions with automatic cost calculation based on duration

It is designed to automate parking management for small parking facilities or serve as the backend for a parking application.

To run the project:
- git clone https://github.com/TwoUfo/Shmego-API.git
- pip install -r requirements.txt
- export PYTHONPATH=./
- python run.py

# Endpoints:

**Cars**
GET /cars – Retrieve a list of all registered cars.
POST /cars – Add a new car to the system.
GET /cars/{license_plate} – Get details of a specific car by license plate.
PUT /cars/{license_plate} – Update the information of a specific car.

**Parking Spots**
GET /spots – Retrieve a list of all parking spots with their occupancy status.
POST /spots – Create a new parking spot.
GET /spots/{spot_number} – Get details of a specific parking spot.
PUT /spots/{spot_number} – Update information (e.g. availability) of a parking spot.

**Parking Sessions**
GET /sessions – Get a list of all parking sessions.
GET /sessions/{id} – Retrieve details of a specific parking session by ID.
POST /sessions/check-in – Start a new parking session (car checks into a spot).
POST /sessions/check-out/{car_license_plate} – End a parking session and calculate the cost (car checks out).
