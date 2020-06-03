import pytest
import os
import uuid
from visit_counter import const, errors
from visit_counter.storage import FileStorage, MySQLStorage, check_type


@pytest.fixture()
def mysql_storage():
    storage = MySQLStorage('test_storage')
    storage.connect(**const.default_kwargs)
    return storage


@pytest.fixture()
def file_storage():
    return FileStorage('test_storage')


def test_check_type_correctly_file():
    storage = check_type(const.StorageType('file'), const.default_kwargs, 'test_type')
    assert storage is not None
    assert isinstance(storage, FileStorage)
    os.remove('test_type')


def test_check_type_correctly_sql():
    storage = check_type(const.StorageType('sql'), const.default_kwargs, 'test_type')
    assert storage is not None
    assert isinstance(storage, MySQLStorage)

def test_check_file_is_exist(file_storage):
    some_dict = { 'foo': 'bar' }
    file_storage.check_file_exists('test_exist', some_dict)
    assert os.path.exists('test_exist')
    os.remove('test_exist')


def test_load_data_file(file_storage):
    some_data = file_storage.load_data()
    for key in const.default_dict.keys():
        assert some_data[key] is not None
    assert some_data is not None


def test_upload_data_file(file_storage):
    file_storage.update_data('/test','1','01.01.0001', 'Mozilla/5.0', file_storage.site)
    assert os.path.exists(file_storage.site)
    assert file_storage.get_data_by('path') is not None


def test_get_data_by_something_file(file_storage):
    some_data = file_storage.get_data_by('foo')
    assert isinstance(some_data, list)
    assert len(some_data) == 0


def test_get_data_by_some_value_file(file_storage):
    test1 = len(file_storage.get_data_by('id'))
    unique_id = str(uuid.uuid4())
    file_storage.update_data('/test',unique_id,'01.01.0001', 'Mozilla/5.0', file_storage.site)
    data_to_get = file_storage.get_data_by('id')
    assert isinstance(data_to_get, list)
    assert len(data_to_get) == test1 + 1


def test_connection_success(mysql_storage):
    assert mysql_storage.connection is not None
    assert mysql_storage is not None


def test_connection_failed():
    storage = MySQLStorage('test_failed')
    try:
        storage.connect(host='localhost', user='root')
    except errors.ConnectionError as e:
        assert e.http_code == 400
        assert e.message is not None


def test_load_data_sql(mysql_storage):
    some_data = mysql_storage.load_data()[0]
    assert some_data is not None
    assert list(some_data.keys()).__contains__('id')


def test_update_data_sql(mysql_storage):
    mysql_storage.update_data('/test_storage1', '1', '01.01.0001', 'Mozilla/5.0', mysql_storage.site)
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
