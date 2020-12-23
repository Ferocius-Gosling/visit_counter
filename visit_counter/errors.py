class APIError(Exception):
    http_code = 500
    message: str


class SetUpError(Exception):
    http_code = 500
    message: str


class ConnectionError(SetUpError):
    http_code = 400
    message = 'Connection error. Check your database connection settings'


class CreateFileError(SetUpError):
    http_code = 400
    message = 'Create file error.'


class FileConnectionArgsError(SetUpError):
    http_code = 400
    message = 'Not found file_from. Check your connection settings'


class SQLConnectionArgsError(SetUpError):
    http_code = 400
    message = 'Not found host/user/pass/db-name.' \
              ' Check your database connection settings'


class FileStructureError(SetUpError):
    http_code = 400
    message = 'File contains invalid json-body'


class InvalidArgumentError(APIError):
    def __init__(self, argument):
        self.message = self.message.format(argument)

    http_code = 400
    message = 'Invalid argument {}'
