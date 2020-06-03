from visit_counter import const
from visit_counter.managers import StatDateManager, StatUserManager
from collections import Counter
from datetime import datetime


class VisitCounter:
    def __init__(self, data_storage):
        self.data_storage = data_storage

    def make_visit(self, path, user_id, user_agent, domain):
        self.data_storage.update_data(path, user_id, get_date(), user_agent, domain)

    def get_unique_user_stats(self):
        data = self.data_storage.get_data_by('id')
        return len(Counter(data).keys())

    def get_date_stats(self, time_section):
        selected_data = self.data_storage.get_data_by('date')
        manager = StatDateManager(selected_data)
        stats = manager.count(time_section, get_date())
        return stats

    def get_user_stats(self, user_id):
        selected_data = self.data_storage.get_data_by('id')
        manager = StatUserManager(selected_data)
        stats = manager.count(user_id)
        return stats


def get_date():
    now = datetime.now()
    return now.strftime("%H:%d.%W.%m.%Y")
