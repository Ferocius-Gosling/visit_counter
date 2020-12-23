import pymysql
import json
import abc
import os
from visit_counter import const, errors, utils


class AbstractStorage(abc.ABC):
    def connect(self):
        raise NotImplementedError

    def load_data(self):
        raise NotImplementedError

    def update_data(self, path, user_id, date, user_agent, domain):
        raise NotImplementedError

    def get_data_by(self, column_name):
        raise NotImplementedError


class MySQLStorage(AbstractStorage):
    def __init__(self, site, **connection_kwargs):
        self.connection = None
        self.site = site
        try:
            self.host = connection_kwargs['host']
            self.user = connection_kwargs['user']
            self.password = connection_kwargs['password']
            self.db = connection_kwargs['db_name']
        except KeyError:
            raise errors.SQLConnectionArgsError()

    def check_table(self):
        with self.connection:
            cur = self.connection.cursor()
            cur.execute('SELECT 1 FROM visits')
            cur.fetchall()

    def create_table(self):
        with self.connection:
            cur = self.connection.cursor()
            cur.execute("CREATE TABLE visits (path VARCHAR(64) NOT NULL,"
                        " id VARCHAR(64) NOT NULL, date VARCHAR(16) NOT NULL,"
                        " user_agent VARCHAR(136) NOT NULL, domain VARCHAR(64)"
                        " NOT NULL)")

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db,
                cursorclass=pymysql.cursors.DictCursor)
        except pymysql.err.DatabaseError:
            raise errors.ConnectionError()
        try:
            self.check_table()
        except pymysql.err.ProgrammingError:
            self.create_table()

    def load_data(self):
        with self.connection:
            cur = self.connection.cursor()
            cur.execute('SELECT * FROM visits WHERE domain=%s', self.site)
            count_data = cur.fetchall()
            return count_data

    def get_data_by(self, column_to_select):
        if not utils.check_in_keys_meta(column_to_select):
            raise errors.InvalidArgumentError(column_to_select)
        with self.connection:
            cur = self.connection.cursor()
            cur.execute('SELECT %s FROM visits WHERE domain="%s"'
                        % (column_to_select, self.site))
            data = cur.fetchall()
            data_to_get = []
            for item in list(data):
                data_to_get.append(item[column_to_select])
            return data_to_get

    def update_data(self, path, user_id, date, user_agent, domain):
        with self.connection:
            cur = self.connection.cursor()
            columns = 'path, id, date, user_agent, domain'
            cur.execute("INSERT INTO visits (%s) VALUE ('%s', '%s', '%s',"
                        " '%s', '%s')"
                        % (columns, path, user_id, date, user_agent, domain))


class FileStorage(AbstractStorage):
    def __init__(self, site, **connection_kwargs):
        self.site = site
        try:
            self.file_from = connection_kwargs['db_name']
        except KeyError:
            raise errors.FileConnectionArgsError()

    def connect(self):
        try:
            if not os.path.exists(self.file_from):
                with open(self.file_from, 'w+') as write_file:
                    json.dump(const.default_dict, write_file)
        except KeyError:
            raise errors.FileStructureError()
        except OSError:
            raise errors.CreateFileError()

    def load_data(self):
        with open(self.file_from, 'r') as read_file:
            return json.load(read_file)

    def update_data(self, path, user_id, date, user_agent, domain):
        data = self.load_data()
        metadata = utils.get_meta_dict(
            user_id=user_id,
            date=date,
            path=path,
            domain=domain,
            user_agent=user_agent)
        data['meta'].append(metadata)
        with open(self.file_from, 'w+') as write_file:
            json.dump(data, write_file)

    def get_data_by(self, column_to_select):
        if not utils.check_in_keys_meta(column_to_select):
            raise errors.InvalidArgumentError(column_to_select)
        data = self.load_data()
        data_to_get = []
        for item in data['meta']:
            if item['domain'] == self.site:
                data_to_get.append(item[column_to_select])
        return data_to_get


def check_type(type_storage, connection_kwargs, domain):
    storage = None
    if type_storage == const.StorageType('sql'):
        storage = MySQLStorage(domain, **connection_kwargs)
    elif type_storage == const.StorageType('file'):
        storage = FileStorage(domain, **connection_kwargs)
    storage.connect()
    return storage
