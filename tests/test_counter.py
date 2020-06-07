from visit_counter.counter import VisitCounter
from visit_counter.const import default_kwargs, TimeSection
from visit_counter.storage import FileStorage, MySQLStorage
import uuid
import pytest


@pytest.fixture()
def test_counter():
    storage = FileStorage('test', db_name='test')
    storage.connect()
    return VisitCounter(storage)


@pytest.fixture()
def counter_file():
    storage = MySQLStorage('test', **default_kwargs)
    storage.connect()
    return VisitCounter(storage)


@pytest.fixture()
def user_id():
    return str(uuid.uuid4())


def test_count_5_times(test_counter, user_id):
    total = test_counter.get_date_stats(TimeSection.total)
    yearly = test_counter.get_date_stats(TimeSection.yearly)
    monthly = test_counter.get_date_stats(TimeSection.monthly)
    daily = test_counter.get_date_stats(TimeSection.daily)
    for _ in range(5):
        test_counter.make_visit('/test', user_id, 'Mozilla/5.0', 'test')

    assert test_counter.get_date_stats(TimeSection.daily) == daily + 5
    assert test_counter.get_date_stats(TimeSection.total) == total + 5
    assert test_counter.get_date_stats(TimeSection.monthly) == monthly + 5
    assert test_counter.get_date_stats(TimeSection.yearly) == yearly + 5


def test_next_id(test_counter):
    unique_count = test_counter.get_unique_user_stats()
    user_id = str(uuid.uuid4())
    test_counter.make_visit('/test', user_id, 'Mozilla/5.0', 'test')
    assert test_counter.get_unique_user_stats() == unique_count + 1


def test_get_stats_total(test_counter, user_id):
    test = test_counter.get_date_stats(TimeSection.total)

    for _ in range(5):
        test_counter.make_visit('/test', user_id, 'Mozilla/5.0', 'test')
    stats = test_counter.get_date_stats(TimeSection.total)

    assert stats == test + 5


def test_get_stats_yearly(test_counter, user_id):
    test = test_counter.get_date_stats(TimeSection.yearly)

    for _ in range(5):
        test_counter.make_visit('/test', user_id, 'Mozilla/5.0', 'test')
    stats = test_counter.get_date_stats(TimeSection.yearly)

    assert stats == test + 5


def test_get_stats_monthly(test_counter, user_id):
    test = test_counter.get_date_stats(TimeSection.monthly)

    for _ in range(5):
        test_counter.make_visit('/test', user_id, 'Mozilla/5.0', 'test')
    stats = test_counter.get_date_stats(TimeSection.monthly)

    assert stats == test + 5


def test_get_stats_user_id(test_counter):
    unique_user_id = str(uuid.uuid4())
    for _ in range(5):
        test_counter.make_visit('/test', unique_user_id, 'Mozilla/5.0', 'test')
    stats = test_counter.get_user_stats(unique_user_id)
    assert stats == 5


def test_sql_counter_create_correctly(counter_file):
    assert counter_file.data_storage is not None
    assert counter_file is not None


def test_count_10_times_sql(counter_file, user_id):
    total = counter_file.get_date_stats(TimeSection.total)
    yearly = counter_file.get_date_stats(TimeSection.yearly)
    monthly = counter_file.get_date_stats(TimeSection.monthly)
    daily = counter_file.get_date_stats(TimeSection.daily)
    for _ in range(5):
        counter_file.make_visit('/test', user_id, 'Mozilla/5.0', 'test')

    assert counter_file.get_date_stats(TimeSection.daily) == daily + 5
    assert counter_file.get_date_stats(TimeSection.total) == total + 5
    assert counter_file.get_date_stats(TimeSection.monthly) == monthly + 5
    assert counter_file.get_date_stats(TimeSection.yearly) == yearly + 5
