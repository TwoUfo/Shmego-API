# Status Codes
STATUS_OK = 200
STATUS_CREATED = 201
STATUS_NO_CONTENT = 204
STATUS_BAD_REQUEST = 400
STATUS_NOT_FOUND = 404
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN = 403
STATUS_SERVER_ERROR = 500


# Car messages
MSG_CAR_ADDED = "Car added"
MSG_CAR_UPDATED = "Car updated"
ERR_CAR_EXISTS = "Car already exists"

# Spot messages
MSG_SPOT_ADDED = "Parking spot added"
MSG_SPOT_UPDATED = "Parking spot updated"
ERR_SPOT_OCCUPIED = "Parking spot is already occupied"
ERR_OBJECT_NOT_FOUND = "Object {} not found"


# Session messages
MSG_SESSION_STARTED = "Parking session started"
MSG_ALREADY_CHECKED_OUT = "Already checked out."
MSG_CHECKED_OUT_SUCCESS = "Checked out successfully."


# Keys
KEY_ID = "id"
KEY_CAR = "Car with license plate '{}'"
KEY_SPOT = "Spot with number '{}'"
KEY_SESSION = "Session with car license plate '{}'"
KEY_OWNER = "owner"
KEY_LICENSE_PLATE = "license_plate"
KEY_BRAND = "brand"
KEY_MODEL = "model"
KEY_OWNER = "owner"
KEY_NUMBER = "number"
KEY_IS_OCCUPIED = "is_occupied"
KEY_CAR_ID = "car_id"
KEY_SPOT_ID = "spot_id"
KEY_CHECK_IN = "check_in_time"
KEY_CHECK_OUT = "check_out_time"
KEY_COST = "cost"
KEY_SESSION_ID = "session_id"
KEY_CAR_LICENSE_PLATE = "car_license_plate"
KEY_SPOT_NUMBER = "spot_number"
KEY_ERROR = "error_message"
KEY_DURATION_HOURS = "duration_hours"
KEY_CHECK_IN = "check_in"
KEY_CHECK_OUT = "check_out"
KEY_VIP = "vip"
KEY_START_DATE = "start_date"
KEY_END_DATE = "end_date"
KEY_USER_ID = "id"
KEY_ROLE = "role"

# Other
VIP_SPOT_PRICE = 40
DEFAULT_SPOT_PRICE = 25
PAGE = "page"
PER_PAGE = "per_page"
PAGE_DEFAULT = 1
PER_PAGE_DEFAULT = 6
TOKEN_IS_MISSING = "Token is missing"
SESSION_ID_IS_MISSING = "Session ID is missing"
SESSION_EXPIRED = "Session expired"
REQUEST_DENIED = "Request denied, insufficient permissions"
LOGIN_FAILED_INVALID_CREDENTIALS = "Login failed, invalid credentials"
LOGIN_FAILED = "Login failed"
LOGOUT_FAILED = "Logout failed"
INVALID_PASSWORD = "Invalid password"
REFRESH_TOKEN_MISSING = "Refresh token is missing"
INVALID_REFRESH_TOKEN = "Invalid refresh token"
REFRESH_TOKEN_FAILED = "Failed to refresh token"
LOGIN_SUCCESS = "Logged in successfully"
LOGIN_SUCCESS_INFO = "Login successful user ID: {}"
LOG_OUT_SUCCESS = "Logged out successfully"
TOKEN_REFRESHED = "Token refreshed successfully"
OBJECT_NOT_FOUND = "{} not found"

# Auth constants
ACCESS_TOKEN = "access_token"
REFRESH_TOKEN = "refresh_token"
SESSION_ID = "session_id"
EIGHT_HOURS = 28800  # 8 hours in seconds
ENCODE_ALGORITHM = "HS256"

