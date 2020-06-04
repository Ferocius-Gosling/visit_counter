class APIError(Exception):
    http_code = 500
    message: str


class SetUpError(Exception):
    http_code = 500
    message : str


class ConnectionError(SetUpError):
    http_code = 400
    message = 'Connection error. Check your database connection settings'


class CreateFileError(SetUpError):
    http_code = 400
    message = 'Create file error.'


class ConnectionArgsError(APIError):
    http_code = 400
    message = 'Wrong connection args'
