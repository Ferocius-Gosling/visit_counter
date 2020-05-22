from enum import Enum


class StorageType(Enum):
    sql = 'sql'
    file = 'file'

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)

    def __str__(self):
        return self.value


class Metadata:
    def __init__(self, user_id, date, path, domain, user_agent):
        self.meta = visit_dict
        self.meta['id'] = user_id
        self.meta['date'] = date
        self.meta['path'] = path
        self.meta['domain'] = domain
        self.meta['user_agent'] = user_agent


keys_storage = ['total', 'yearly', 'monthly',
                'daily', 'last_id', 'domain', 'last_visit']

keys_counter = ['daily', 'monthly', 'yearly']

default_dict = {
            'total': 0,
            'yearly': 0,
            'monthly': 0,
            'daily': 0,
            'last_id': 0,
            'last_visit': '01.01.1970',
            'meta': []
}

visit_dict = {
    'id': 0,
    'date': '01.01.1970',
    'path': '',
    'domain': '',
    'user_agent': ''
}
