from collections import defaultdict
from data_storage import AbstractStorage
from datetime import datetime


class Counter:
    def __init__(self, file_date, way_from):
        self.data_storage = AbstractStorage(file_date)
        self.count_data = self.data_storage.load_data('count_visits', way_from)
        self.keys = ['daily', 'monthly', 'yearly']

    def upload_metadata(self, way, user_id):
        self.data_storage.insert_data(user_id, get_date(), way)

    def make_count(self):
        self.count_data['total'] += 1
        current_visit = get_date()
        self.compute_count(current_visit)
        self.count_data['last_visit'] = current_visit
        self.data_storage.update_data(self.count_data)
        return self.count_data

    def compute_count(self, current_visit):
        split = 0
        for key in self.keys:
            if current_visit[split:] != self.count_data['last_visit'][split:]:
                self.count_data[key] = 1
            else:
                self.count_data[key] += 1
            split += 3

    def next_id(self):
        self.count_data['last_id'] += 1
        return self.count_data['last_id']


def get_date():
    now = datetime.now()
    return now.strftime("%d.%m.%Y")