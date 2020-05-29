from visit_counter import storage, const
from datetime import datetime
from collections import Counter


class VisitCounter:
    def __init__(self, domain, type_storage, connection_kwargs=const.default_kwargs):
        self.type_storage = type_storage
        self.data_storage = storage.check_type(type_storage, connection_kwargs, domain)
        self.count_data = self.data_storage.load_data()

    def upload_metadata(self, path, user_id, user_agent, domain):
        self.data_storage.insert_data(path, user_id, get_date(), user_agent, domain)

    def upload_metadata_file(self, path, user_id, user_agent, domain):
        metadata = const.Metadata(user_id, get_date(), path, domain, user_agent)
        self.count_data['meta'].append(metadata.meta)

    def make_visit(self, path, user_id, user_agent, domain, is_unique=False):
        self.count_data['total'] += 1
        if is_unique:
            self.__unique_user_increment()
        current_visit = get_date()
        self.__compute_count(current_visit)
        self.count_data['last_visit'] = current_visit
        if self.type_storage == const.StorageType('sql'):
            self.upload_metadata(path, user_id, user_agent, domain)
        else:
            self.upload_metadata_file(path, user_id, user_agent, domain)
        self.data_storage.update_data(self.count_data)
        return self.count_data

    def __compute_count(self, current_visit):
        split = 0
        for key in const.keys_date:
            if current_visit[split:] != self.count_data['last_visit'][split:]:
                self.count_data[key] = 1
            else:
                self.count_data[key] += 1
            split += 3

    def __unique_user_increment(self):
        self.count_data['last_id'] += 1

    def get_stats(self, column_to_count, item_to_count):
        stats = self.count_data
        selected_data = self.data_storage.get_data_by(column_to_count)
        item_count = Counter(selected_data)
        stats['selected'] = item_count[item_to_count]
        return stats


def get_date():
    now = datetime.now()
    return now.strftime("%d.%m.%Y")
