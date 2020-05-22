import pymysql
import json
import abc
import os
from visit_counter import const


class AbstractStorage(abc.ABC):
    def load_data(self):
        raise NotImplementedError

    def update_data(self, count_data):
        raise NotImplementedError

    def get_data_by(self, column_name):
        raise NotImplementedError
    # def insert_data(self, user_id, date, way):
    #     raise NotImplementedError


class MySQLStorage(AbstractStorage):
    def __init__(self, file_data, path_from):
        self.file_data = pymysql.connect(host='localhost',
                                         user='root',
                                         password='root',
                                         db=file_data,
                                         cursorclass=pymysql.cursors.DictCursor)
        self.path_from = path_from

    def load_data(self):
        with self.file_data:
            cur = self.file_data.cursor()
            cur.execute('SELECT * FROM count_visits WHERE domain=%s', self.path_from)
           # fetched =
            count_data = cur.fetchall()[0]
        return count_data

    def update_data(self, count_data):
        with self.file_data:
            cur = self.file_data.cursor()
            query = 'UPDATE count_visits SET '
            where = ' WHERE domain=\'' + self.path_from + "'"
            for key in const.keys_storage:
                cur.execute(query + key + '=%s' + where, count_data[key])

    def get_data_by(self, column_name):
        with self.file_data:
            cur = self.file_data.cursor()
            select_from = 'SELECT ' + column_name + ' FROM user_visits '
            cur.execute(select_from + 'WHERE domain=%s',self.path_from)
            data = cur.fetchall()
            data_to_get = []
            for item in list(data):
                data_to_get.append(item[column_name])
            return data_to_get

    def insert_data(self, path, user_id, date, user_agent, domain):
        with self.file_data:
            cur = self.file_data.cursor()
            columns = 'path, id, date, user_agent, domain'
            query = "INSERT INTO user_visits (" + columns + ") VALUE "
            value = "('{}','{}','{}','{}','{}')".format(path, user_id, date, user_agent, domain)
            cur.execute(query + value)


class FileStorage(AbstractStorage):
    def __init__(self, domain):
        self.count_data = domain

    def _check_file_exists(self, file_from, def_dict=const.default_dict):
        if not os.path.exists(file_from):
            with open(file_from, 'w+') as write_file:
                json.dump(def_dict, write_file)

    def load_data(self):
        self._check_file_exists(self.count_data)
        with open(self.count_data, 'r') as read_file:
            return json.load(read_file)

    def update_data(self, count_data):
        with open(self.count_data, 'w+') as write_file:
            json.dump(count_data, write_file)

    def get_data_by(self, column_name):
        data = self.load_data()
        data_to_get = []
        for item in data['meta']:
            data_to_get.append(item[column_name])
        return data_to_get

    def insert_data(self, metadata):    
        pass

    # def insert_data(self, user_id, date, way):
    #     # self._check_file_exists(self.visits_data, const.visit_dict)
    #     # with open(self.visits_data, 'r') as read_file:
    #     #   visits = json.load(read_file)
    #     visits['meta'].append()
    #     with open(self.visits_data, 'w+') as write_file:
    #         json.dump(visits, write_file)


def check_type(type_storage, file_data, domain):
    if type_storage == const.StorageType('sql'):
        return MySQLStorage(file_data, domain)
    if type_storage == const.StorageType('file'):
        return FileStorage(domain)
    raise IOError
