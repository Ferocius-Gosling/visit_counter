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


class MySQLStorage(AbstractStorage):
    def __init__(self, connection_kwargs: dict, site):
        self.connection = self.__connect(connection_kwargs)
        self.site = site

    @staticmethod
    def __connect(connect_kwargs: dict):
        return pymysql.connect(host=connect_kwargs['host'],
                               user=connect_kwargs['user'],
                               password=connect_kwargs['password'],
                               db=connect_kwargs['db_name'],
                               cursorclass=pymysql.cursors.DictCursor)

    def load_data(self):
        with self.connection:
            cur = self.connection.cursor()
            self.__check_domain_exist(cur)
            cur.execute('SELECT * FROM count_visits WHERE domain=%s', self.site)
            count_data = cur.fetchall()[0]
            return count_data

    @staticmethod
    def __insert_new_domain(cursor, site):
        columns = 'total, daily, monthly, yearly, last_id, domain, last_visit'
        cursor.execute('INSERT INTO count_visits (%s) VALUE (%s,%s,%s,%s,%s,"%s","%s")'
                       %(columns, 0, 0, 0, 0, 0, site, '01.01.1970'))

    def __check_domain_exist(self, cursor):
        cursor.execute('SELECT * FROM count_visits WHERE domain=%s', self.site)
        data = cursor.fetchall()
        if data == ():
            self.__insert_new_domain(cursor, self.site)

    def update_data(self, count_data):
        with self.connection:
            cur = self.connection.cursor()
            for key in const.keys_storage:
                cur.execute('UPDATE count_visits SET %s="%s" WHERE domain="%s"' % (key, count_data[key], self.site))

    def get_data_by(self, column_to_select):
        if not const.check_in_keys_meta(column_to_select):
            return []
        with self.connection:
            cur = self.connection.cursor()
            cur.execute('SELECT %s FROM user_visits WHERE domain="%s"' % (column_to_select, self.site))
            data = cur.fetchall()
            data_to_get = []
            for item in list(data):
                data_to_get.append(item[column_to_select])
            return data_to_get

    def insert_data(self, path, user_id, date, user_agent, domain):
        with self.connection:
            cur = self.connection.cursor()
            columns = 'path, id, date, user_agent, domain'
            cur.execute("INSERT INTO user_visits (%s) VALUE ('%s', '%s', '%s', '%s', '%s')"
                        % (columns, path, user_id, date, user_agent, domain))


class FileStorage(AbstractStorage):
    def __init__(self, site):
        self.site = site

    def _check_file_exists(self, file_from, def_dict=const.default_dict):
        if not os.path.exists(file_from):
            with open(file_from, 'w+') as write_file:
                json.dump(def_dict, write_file)

    def load_data(self):
        self._check_file_exists(self.site)
        with open(self.site, 'r') as read_file:
            return json.load(read_file)

    def update_data(self, count_data):
        with open(self.site, 'w+') as write_file:
            json.dump(count_data, write_file)

    def get_data_by(self, column_name):
        data = self.load_data()
        data_to_get = []
        for item in data['meta']:
            data_to_get.append(item[column_name])
        return data_to_get

    def insert_data(self, metadata):    
        pass


def check_type(type_storage, file_data, domain):
    if type_storage == const.StorageType('sql'):
        return MySQLStorage(file_data, domain)
    if type_storage == const.StorageType('file'):
        return FileStorage(domain)
    raise IOError
