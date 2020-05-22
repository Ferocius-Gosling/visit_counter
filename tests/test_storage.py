import pytest
import os
from visit_counter import const
from visit_counter.storage import FileStorage, MySQLStorage


@pytest.fixture()
def mysql_storage():
    return MySQLStorage('count_data', 'test_storage')


@pytest.fixture()
def file_storage():
    return FileStorage('test_storage')


def test_check_file_is_exist(file_storage):
    some_dict = { 'foo': 'bar' }
    file_storage._check_file_exists('test_exist', some_dict)
    assert os.path.exists('test_exist')
    os.remove('test_exist')


def test_load_data_file(file_storage):
    some_data = file_storage.load_data()
    for key in const.default_dict.keys():
        assert some_data[key] is not None
    assert some_data is not None


def test_upload_data_file(file_storage):
    some_data = const.default_dict
    file_storage.update_data(some_data)
    assert os.path.exists(file_storage.count_data)
    assert some_data == file_storage.load_data()


def test_get_data_by_something_file(file_storage):
    some_data = file_storage.get_data_by('foo')
    assert isinstance(some_data, list)
    assert len(some_data) == 0


def test_get_data_by_some_value_file(file_storage):
    some_data = file_storage.load_data()
    some_data['meta'].append(const.visit_dict)
    file_storage.update_data(some_data)
    data_to_get = file_storage.get_data_by('id')
    assert isinstance(data_to_get, list)
    assert len(data_to_get) == 1


def test_load_data_sql(mysql_storage):
    some_data = mysql_storage.load_data()
    assert some_data is not None
    assert list(some_data.keys()) == const.keys_storage


def test_update_data_sql(mysql_storage):
    some_data = mysql_storage.load_data()
    total = some_data['total']
    some_data['total'] += 1
    mysql_storage.update_data(some_data)
    assert mysql_storage.load_data()['total'] == total + 1


def test_insert_data_sql(mysql_storage):
    mysql_storage.insert_data('/test_storage1', '1', '01.01.0001', 'Mozilla/5.0', mysql_storage.path_from)
    some_data = mysql_storage.get_data_by('date')
    assert some_data is not None
    assert len(some_data) != 0
    assert some_data[0] == '01.01.0001'


def test_get_data_by_something_sql(mysql_storage):
    data = mysql_storage.get_data_by('foo')
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_data_by_value_sql(mysql_storage):
    data = mysql_storage.get_data_by('path')
    assert data is not None
    assert isinstance(data, list)
    assert len(data) != 0
    assert data[0] == '/test_storage1'
