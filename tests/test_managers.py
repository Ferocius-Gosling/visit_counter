import pytest
from visit_counter.managers import StatDateManager, StatUserManager
from visit_counter.const import TimeSection


@pytest.fixture()
def data_to_count():
    data = list()
    data.append('01:01.01.01.0001')
    data.append('02:01.01.01.0001')
    data.append('01:02.01.01.0001')
    data.append('01:01.02.01.0001')
    data.append('01:01.01.02.0001')
    data.append('01:01.01.01.0002')
    return data


@pytest.fixture()
def date_manager(data_to_count):
    return StatDateManager(data_to_count)


@pytest.fixture()
def user_manager(data_to_count):
    return StatUserManager(data_to_count)


def test_count_every_time_section(date_manager):
    assert date_manager.count(TimeSection.hourly,
                              '01:01.01.01.0001') == 1
    assert date_manager.count(TimeSection.daily,
                              '01:01.01.01.0001') == 2
    assert date_manager.count(TimeSection.weekly,
                              '01:01.01.01.0001') == 3
    assert date_manager.count(TimeSection.monthly,
                              '01:01.01.01.0001') == 4
    assert date_manager.count(TimeSection.yearly,
                              '01:01.01.01.0001') == 5
    assert date_manager.count(TimeSection.total,
                              '01:01.01.01.0001') == 6


def test_count_user_id(user_manager):
    assert user_manager.count('01:01.01.01.0001') == 1


def test_count_user_id_when_no_match(user_manager):
    assert user_manager.count('01:01.01,01.0001') == 0
