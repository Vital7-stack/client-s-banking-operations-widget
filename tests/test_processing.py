import pytest
from collections import Counter
from src.processing import filter_by_state, sort_by_date, process_bank_search, process_bank_operations


def test_filter_by_state_case_insensitive():
    data = [
        {"state": "executed", "description": "test"},
        {"state": "EXECUTED", "description": "test2"},
        {"state": "canceled", "description": "test3"},
    ]
    assert len(filter_by_state(data, "executed")) == 2
    assert len(filter_by_state(data, "CANCELED")) == 1


def test_sort_by_date_asc():
    data = [
        {"date": "2024-01-03", "description": "c"},
        {"date": "2024-01-01", "description": "a"},
        {"date": "2024-01-02", "description": "b"},
    ]
    sorted_data = sort_by_date(data, reverse=False)
    dates = [t["date"] for t in sorted_data]
    assert dates == ["2024-01-01", "2024-01-02", "2024-01-03"]


def test_process_bank_search_regex_match():
    data = [
        {"description": "Перевод организации"},
        {"description": "перевод организации"},
        {"description": "Оплата услуг"},
    ]
    res = process_bank_search(data, "перевод")
    assert len(res) == 2


def test_process_bank_search_empty_query():
    data = [{"description": "abc"}, {"description": "xyz"}]
    res = process_bank_search(data, "")
    assert res == data


def test_process_bank_operations_counter():
    data = [
        {"description": "Перевод организации"},
        {"description": "Перевод с карты"},
        {"description": "Снятие наличных"},
        {"description": "снятие наличных"},
    ]
    cats = ["Перевод", "снятие"]
    res = process_bank_operations(data, cats)
    assert res["Перевод"] == 2
    assert res["снятие"] == 2