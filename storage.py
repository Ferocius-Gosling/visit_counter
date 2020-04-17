import pymysql
import json
import abc
import os
import const


class AbstractStorage(abc.ABC):
    def load_data(self, file_from):
        raise NotImplementedError

    def update_data(self, count_data):
        raise NotImplementedError

    def insert_data(self, user_id, date, way):
        raise NotImplementedError


class MySQLStorage(AbstractStorage):
    def __init__(self, file_data, way_from):
        self.file_data = pymysql.connect(host='localhost',
                                         user='root',
                                         password='root',
                                         db=file_data,
                                         cursorclass=pymysql.cursors.DictCursor)
        self.way_from = way_from

    def load_data(self, file_from):
        with self.file_data:
            cur = self.file_data.cursor()
            cur.execute('SELECT * FROM ' + file_from + ' WHERE way_from=' + '\'' + self.way_from + '\'')
            count_data = cur.fetchall()[0]
        return count_data

    def update_data(self, count_data):
        with self.file_data:
            cur = self.file_data.cursor()
            query = 'UPDATE count_visits SET '
            where = ' WHERE way_from=\'' + self.way_from + "'"
            for key in const.keys_storage:
                if key == 'way_from' or key == 'last_visit':
                    cur.execute(query + key+'=' + "'{}'".format(count_data[key]) + where)
                else:
                    cur.execute(query + key+'='+'{}'.format(count_data[key]) + where)

    def insert_data(self, user_id, date, way):
        with self.file_data:
            cur = self.file_data.cursor()
            query = "INSERT INTO user_visits (way_from, user_id, date_visit) VALUE "
            value = "('{}',{},'{}')".format(way, user_id, date)
            cur.execute(query + value)


class FileStorage(AbstractStorage):
    def __init__(self, count_data, way_from):
        self.visits_data = count_data
        self.way_from = way_from

    def _check_file_exists(self, file_from, def_dict=const.default_dict):
        if not os.path.exists(file_from):
            with open(file_from, 'w+') as write_file:
                json.dump(def_dict, write_file)

    def load_data(self, file_from):
        self._check_file_exists(self.way_from)
        with open(self.way_from, 'r') as read_file:
            return json.load(read_file)

    def update_data(self, count_data):
        with open(self.way_from, 'w+') as write_file:
            json.dump(count_data, write_file)

    def insert_data(self, user_id, date, way):
        self._check_file_exists(self.visits_data, const.visit_dict)
        with open(self.visits_data, 'r') as read_file:
            visits = json.load(read_file)
        visits['meta'].append([way, user_id, date])
        with open(self.visits_data, 'w+') as write_file:
            json.dump(visits, write_file)


def check_type(type_data, file_data, way_from):
    if type_data == 'sql':
        return MySQLStorage(file_data, way_from)
    if type_data == 'file':
        return FileStorage(file_data, way_from)
    raise IOError
