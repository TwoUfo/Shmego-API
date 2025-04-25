class SessionAlreadyCheckedOut(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code

class ObjectNotFound(Exception):
    def __init__(self, message: str, obj, status_code: int = 404):
        super().__init__(message.format(obj))
        self.status_code = status_code
        
class SpotAlreadyOccupied(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code