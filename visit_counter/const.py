from enum import Enum


class TimeSection(Enum):
    total = 16
    yearly = 12
    monthly = 9
    weekly = 6
    daily = 3
    hourly = 0

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)

    def __str__(self):
        return self.value


class StorageType(Enum):
    sql = 'sql'
    file = 'file'

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)

    def __str__(self):
        return self.value


default_kwargs = {
    'host': 'db4free.net',
    'user': 'ferocius_gos',
    'password': 'qwerty1234',
    'db_name': 'count_data'
}


keys_storage = ['total', 'yearly', 'monthly',
                'daily', 'last_id', 'domain', 'last_visit']

keys_date = ['daily', 'monthly', 'yearly']

keys_meta = ['path', 'id', 'date', 'user_agent', 'domain']

default_dict = {
            'meta': []
}

visit_dict = {
    'id': 0,
    'date': '01.01.1970',
    'path': '',
    'domain': '',
    'user_agent': ''
}
