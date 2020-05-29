from visit_counter.counter import VisitCounter, get_date
from visit_counter.const import StorageType, default_kwargs
import uuid
import pytest
import os


@pytest.fixture()
def test_counter():
    return VisitCounter('test', StorageType('file'), default_kwargs)


@pytest.fixture()
def counter_file():
    return VisitCounter('test', StorageType('sql'), default_kwargs)


@pytest.fixture()
def user_id():
    return str(uuid.uuid4())


def test_count_10_times(test_counter, user_id):
    total = test_counter.count_data['total']
    yearly = test_counter.count_data['yearly']
    monthly = test_counter.count_data['monthly']
    daily = test_counter.count_data['daily']
    for _ in range(5):
        test_counter.make_visit('/test', user_id, 'Mozilla/5.0', 'test')

    assert test_counter.count_data['daily'] == daily + 5
    assert test_counter.count_data['total'] == total + 5
    assert test_counter.count_data['monthly'] == monthly + 5
    assert test_counter.count_data['yearly'] == yearly + 5


def test_count_with_different_date(user_id):
    counter = VisitCounter('test_date', StorageType('file'), default_kwargs)
    counter.count_data['last_visit'] = '01.01.1970'
    for _ in range(5):
        counter.make_visit('/test', user_id, 'Mozilla/5.0', 'test_date')

    assert counter.count_data['daily'] == 5
    assert counter.count_data['monthly'] == 5
    assert counter.count_data['yearly'] == 5


def test_next_id(test_counter, user_id):
    unique_count = test_counter.count_data['last_id']
    test_counter.make_visit('/test', user_id, 'Mozilla/5.0', 'test', is_unique=True)
    assert test_counter.count_data['last_id'] == unique_count + 1


def test_get_stats_by_path(test_counter, user_id):
    stats = test_counter.get_stats('path', '/test1')
    test1 = stats['selected']
    for _ in range(5):
        test_counter.make_visit('/test1', user_id, 'Mozilla/5.0', 'test')
    stats = test_counter.get_stats('path', '/test1')

    assert test_counter.count_data['daily'] == stats['daily']
    assert test_counter.count_data['total'] == stats['total']
    assert test_counter.count_data['monthly'] == stats['monthly']
    assert test_counter.count_data['yearly'] == stats['yearly']
    assert stats['selected'] == test1 + 5


def test_get_stats_by_user_id(test_counter):
    unique_user_id = str(uuid.uuid4())
    for _ in range(5):
        test_counter.make_visit('/test', unique_user_id, 'Mozilla/5.0', 'test')
    stats = test_counter.get_stats('id', unique_user_id)

    assert test_counter.count_data['daily'] == stats['daily']
    assert test_counter.count_data['total'] == stats['total']
    assert test_counter.count_data['monthly'] == stats['monthly']
    assert test_counter.count_data['yearly'] == stats['yearly']
    assert stats['selected'] == 5


def test_get_stats_by_date_day(test_counter):
    stats = test_counter.get_stats('date', get_date())

    assert test_counter.count_data['daily'] == stats['daily']
    assert test_counter.count_data['total'] == stats['total']
    assert test_counter.count_data['monthly'] == stats['monthly']
    assert test_counter.count_data['yearly'] == stats['yearly']
    assert stats['selected'] == test_counter.count_data['daily']


def test_get_stats_by_user_agent(test_counter, user_id):
    stats2 = test_counter.get_stats('user_agent', 'Mozilla/5.0 (like Gecko)')
    test2 = stats2['selected']
    for _ in range(5):
        test_counter.make_visit('/test', user_id, 'Mozilla/5.0 (like Gecko)', 'test')
    stats = test_counter.get_stats('user_agent', 'Mozilla/5.0 (like Gecko)')

    assert test_counter.count_data['daily'] == stats['daily']
    assert test_counter.count_data['total'] == stats['total']
    assert test_counter.count_data['monthly'] == stats['monthly']
    assert test_counter.count_data['yearly'] == stats['yearly']
    assert stats['selected'] == test2 + 5


def test_sql_counter_create_correctly(counter_file):
    assert counter_file.type_storage == StorageType('sql')
    assert counter_file.count_data is not None
    assert counter_file is not None


def test_count_10_times_sql(counter_file, user_id):
    total = counter_file.count_data['total']
    yearly = counter_file.count_data['yearly']
    monthly = counter_file.count_data['monthly']
    daily = counter_file.count_data['daily']
    for _ in range(5):
        counter_file.make_visit('/test', user_id, 'Mozilla/5.0', 'test')

    assert counter_file.count_data['daily'] == daily + 5
    assert counter_file.count_data['total'] == total + 5
    assert counter_file.count_data['monthly'] == monthly + 5
    assert counter_file.count_data['yearly'] == yearly + 5
