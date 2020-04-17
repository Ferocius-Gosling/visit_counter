from counter import VisitCounter
import pytest
import os


@pytest.fixture()
def test_counter():
    return VisitCounter('count_data', 'test', 'sql')


@pytest.fixture()
def counter_file():
    return VisitCounter('count_data', 'test', 'file')


def test_count_10_times(test_counter):
    total = test_counter.count_data['total']
    yearly = test_counter.count_data['yearly']
    monthly = test_counter.count_data['monthly']
    daily = test_counter.count_data['daily']
    for _ in range(10):
        test_counter.make_count()

    assert test_counter.count_data['daily'] == daily + 10
    assert test_counter.count_data['total'] == total + 10
    assert test_counter.count_data['monthly'] == monthly + 10
    assert test_counter.count_data['yearly'] == yearly + 10


def test_count_with_different_date(test_counter):
    test_counter.count_data['last_visit'] = '01.01.1970'
    for _ in range(10):
        test_counter.make_count()

    assert test_counter.count_data['daily'] == 10
    assert test_counter.count_data['monthly'] == 10
    assert test_counter.count_data['yearly'] == 10


def test_upload_metadata(test_counter):
    try:
        for _ in range(10):
            test_counter.upload_metadata('test', test_counter.count_data['last_id'])
        assert True
    except Exception as e:
        assert False, str(e)


def test_next_id(test_counter):
    last_id = test_counter.count_data['last_id']
    test_counter.next_user_id()
    assert test_counter.count_data['last_id'] == last_id + 1


def test_count_10_times_file(counter_file):
    total = counter_file.count_data['total']
    yearly = counter_file.count_data['yearly']
    monthly = counter_file.count_data['monthly']
    daily = counter_file.count_data['daily']
    for _ in range(10):
        counter_file.make_count()

    assert counter_file.count_data['daily'] == daily + 10
    assert counter_file.count_data['total'] == total + 10
    assert counter_file.count_data['monthly'] == monthly + 10
    assert counter_file.count_data['yearly'] == yearly + 10


def test_upload_metadata_file(counter_file):
    try:
        for _ in range(10):
            counter_file.upload_metadata('test', counter_file.count_data['last_id'])
        assert True
    except Exception as e:
        assert False, str(e)


def test_create_file_when_file_not_exists():
    counter = VisitCounter('count_data', 'test1', 'file')
    assert os.path.exists(counter.data_storage.way_from)
    os.remove(counter.data_storage.way_from)
