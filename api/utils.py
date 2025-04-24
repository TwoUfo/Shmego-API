from flask import make_response, jsonify


def response(message: str = None, data: dict = None, status_code: int = 200) -> dict:
    """
    Function to create a standardized response format for API responses.

    Args:
        
        message (str): Message to be included in the response.
        data (dict, optional): Additional data to be included in the response. Defaults to None.
        status_code (int): HTTP status code.

    Returns:
        dict: A dictionary containing the status code, message, and data.
    """
    return make_response(
        jsonify(
            {
                "status_code": status_code,
                "message": message if message is not None else {},
                "data": data if data is not None else {},
            }
        ),
        status_code,
    )