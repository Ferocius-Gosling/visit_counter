class APIError(Exception):
    http_code = 500
    message: str


class ConnectionError(APIError):
    http_code = 400
    message = 'Connection error. Check your database connection settings'


class CreateFileError(APIError):
    http_code = 400
    message = 'Create file error.'
