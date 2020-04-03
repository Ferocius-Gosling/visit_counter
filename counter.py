import json
from datetime import datetime


class Counter:
    def __init__(self, file_date):
        self.file_data = file_date

    def put_json(self, count_data):
        with open(self.file_data, 'w') as write_file:
            json.dump(count_data, write_file)

    def get_count(self):
        with open(self.file_data, 'r') as read_file:
            count_data = json.load(read_file)
        count_data['total'] += 1
        get_daily_count(count_data)
        get_monthly_count(count_data)
        get_yearly_count(count_data)
        count_data['last_visit'] = get_date()
        with open(self.file_data, 'w') as write_file:
            json.dump(count_data, write_file)
        return count_data


def get_daily_count(count_data):
    current_visit = get_date()
    if current_visit != count_data['last_visit']:
        count_data['daily'] = 1
    else:
        count_data['daily'] += 1


def get_monthly_count(count_data):
    current_visit = get_date()
    if current_visit[3:] != count_data['last_visit'][3:]:
        count_data['monthly'] = 1
    else:
        count_data['monthly'] += 1


def get_yearly_count(count_data):
    current_visit = get_date()
    if current_visit[6:] != count_data['last_visit'][6:]:
        count_data['yearly'] = 1
    else:
        count_data['yearly'] += 1


def get_date():
    now = datetime.now()
    return now.strftime("%d.%m.%Y")