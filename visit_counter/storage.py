import pymysql
import json
import abc
import os
from visit_counter import const, errors


class AbstractStorage(abc.ABC):
    def connect(self, connect_kwargs):
        raise NotImplementedError

    def load_data(self):
        raise NotImplementedError

    def update_data(self, path, user_id, date, user_agent, domain):
        raise NotImplementedError

    def get_data_by(self, column_name):
        raise NotImplementedError


class MySQLStorage(AbstractStorage):
    def __init__(self, site):
        self.connection = None
        self.site = site

    def check_table(self):
        with self.connection:
            cur = self.connection.cursor()
            cur.execute('SELECT 1 FROM visits')
            cur.fetchall()

    def create_table(self):
        with self.connection:
            cur = self.connection.cursor()
            s = 'path VARCHAR(64) NOT NULL, ' \
                'id VARCHAR(64) NOT NULL, ' \
                'date VARCHAR(16) NOT NULL, ' \
                'user_agent VARCHAR(136) NOT NULL, ' \
                'domain VARCHAR(64) NOT NULL'
            cur.execute('CREATE TABLE visits (%s)' % s)

    def connect(self, **connect_kwargs):
        try:
            self.connection = pymysql.connect(
                               host=connect_kwargs['host'],
                               user=connect_kwargs['user'],
                               password=connect_kwargs['password'],
                               db=connect_kwargs['db_name'],
                               cursorclass=pymysql.cursors.DictCursor)
        except KeyError:
            raise errors.SQLConnectionArgsError()
        except:
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
        if not const.check_in_keys_meta(column_to_select):
            raise errors.InvalidArgumentError(column_to_select)
        with self.connection:
            cur = self.connection.cursor()
            cur.execute('SELECT %s FROM visits WHERE domain="%s"' % (column_to_select, self.site))
            data = cur.fetchall()
            data_to_get = []
            for item in list(data):
                data_to_get.append(item[column_to_select])
            return data_to_get

    def update_data(self, path, user_id, date, user_agent, domain):
        with self.connection:
            cur = self.connection.cursor()
            columns = 'path, id, date, user_agent, domain'
            cur.execute("INSERT INTO visits (%s) VALUE ('%s', '%s', '%s', '%s', '%s')"
                        % (columns, path, user_id, date, user_agent, domain))


class FileStorage(AbstractStorage):
    def __init__(self, site):
        self.site = site

    def connect(self, file_from, def_dict=const.default_dict):
        try:
            if not os.path.exists(file_from):
                with open(file_from, 'w+') as write_file:
                    json.dump(def_dict, write_file)
            data = self.load_data()
            flag = data['meta']
        except KeyError:
            raise errors.FileStructureError()
        except:
            raise errors.CreateFileError()

    def load_data(self):
        with open(self.site, 'r') as read_file:
            return json.load(read_file)

    def update_data(self, path, user_id, date, user_agent, domain):
        data = self.load_data()
        metadata = const.get_meta_dict(
            user_id=user_id,
            date=date,
            path=path,
            domain=domain,
            user_agent=user_agent)
        data['meta'].append(metadata)
        with open(self.site, 'w+') as write_file:
            json.dump(data, write_file)

    def get_data_by(self, column_to_select):
        if not const.check_in_keys_meta(column_to_select):
            raise errors.InvalidArgumentError(column_to_select)
        data = self.load_data()
        data_to_get = []
        for item in data['meta']:
            data_to_get.append(item[column_to_select])
        return data_to_get


def check_type(type_storage, connection_kwargs, domain):
    storage = None
    if type_storage == const.StorageType('sql'):
        storage = MySQLStorage(domain)
    elif type_storage == const.StorageType('file'):
        storage = FileStorage(domain)
        connection_kwargs = {'file_from': domain}
    storage.connect(**connection_kwargs)
    return storage
