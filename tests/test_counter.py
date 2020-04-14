from counter import Counter
import pytest
import json


def test_count_10_times():
    test_data = {'total': 20,
                 'daily': 10,
                 'monthly': 0,
                 'yearly': 0,
                 'last_visit': '01.01.2000'}
    counter = Counter('tests.txt')
    counter.put_json(test_data)

    for i in range(10):
        counter.make_count()
    with open(counter.file_data) as file:
        count_data = json.load(file)
    assert count_data['daily'] == 10
    assert count_data['total'] == 30
    assert count_data['monthly'] == 10
    assert count_data['yearly'] == 10
