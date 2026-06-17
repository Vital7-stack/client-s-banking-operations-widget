from collections import Counter
from src.processing import filter_by_status, sort_by_date, count_operations_by_category


def test_filter_by_status_state_key():
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
    ]
    res = filter_by_status(data, "EXECUTED")
    assert len(res) == 2
    assert all(t["state"] == "EXECUTED" for t in res)


def test_filter_by_status_status_key():
    data = [
        {"id": 1, "status": "EXECUTED"},
        {"id": 2, "status": "PENDING"},
        {"id": 3, "status": "EXECUTED"},
    ]
    res = filter_by_status(data, "EXECUTED")
    assert len(res) == 2


def test_filter_by_status_empty():
    res = filter_by_status([], "EXECUTED")
    assert res == []


def test_sort_by_date_ascending():
    data = [
        {"date": "2024-03-01"},
        {"date": "2024-01-01"},
        {"date": "2024-02-01"},
    ]
    res = sort_by_date(data, ascending=True)
    dates = [t["date"] for t in res]
    assert dates == ["2024-01-01", "2024-02-01", "2024-03-01"]


def test_sort_by_date_descending():
    data = [
        {"date": "2024-03-01"},
        {"date": "2024-01-01"},
        {"date": "2024-02-01"},
    ]
    res = sort_by_date(data, ascending=False)
    dates = [t["date"] for t in res]
    assert dates == ["2024-03-01", "2024-02-01", "2024-01-01"]


def test_count_operations_by_category():
    data = [
        {"category": "food"},
        {"category": "transport"},
        {"category": "food"},
        {"category": None},
        {},
    ]
    counter = count_operations_by_category(data)
    assert counter["food"] == 2
    assert counter["transport"] == 1
    assert "None" not in counter


def test_count_operations_empty():
    counter = count_operations_by_category([])
    assert isinstance(counter, Counter)
    assert len(counter) == 0
