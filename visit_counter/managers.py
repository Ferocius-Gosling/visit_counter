from visit_counter import const, counter
import abc


class StatManager(abc.ABC):
    def count(self, type_of_count):
        raise NotImplementedError


class StatDateManager(StatManager):
    def __init__(self, data):
        self.data = data

    def count(self, time_section, date_to_check):
        stat = 0
        for visit in self.data:
            if visit[time_section.value:] == date_to_check[time_section.value:]:
                stat += 1
        return stat


class StatUserManager(StatManager):
    def __init__(self, data):
        self.data = data

    def count(self, user_id):
        stat = 0
        for visit in self.data:
            if visit == user_id:
                stat += 1
        return stat