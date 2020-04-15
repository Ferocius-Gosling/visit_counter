from counter import Counter
import pytest
import pymysql


@pytest.fixture()
def test_counter():
    return Counter('count_data', 'test')


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
    except TypeError:
        assert False
    except SyntaxError:
        assert False


def test_next_id(test_counter):
    last_id = test_counter.count_data['last_id']
    test_counter.next_user_id()
    assert test_counter.count_data['last_id'] == last_id + 1

