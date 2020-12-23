class StatManager:
    def __init__(self, data):
        self.data = data


class StatDateManager(StatManager):
    def count(self, time_section, date_to_check):
        stat = 0
        for visit in self.data:
            if visit[time_section.value:] == \
                    date_to_check[time_section.value:]:
                stat += 1
        return stat


class StatUserManager(StatManager):
    def count(self, user_id):
        stat = 0
        for visit in self.data:
            if visit == user_id:
                stat += 1
        return stat
