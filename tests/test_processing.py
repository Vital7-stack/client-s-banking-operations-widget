from typing import Any, Dict, List
import pytest
from src.processing import (
    filter_by_state,
    sort_by_date,
    process_transactions,
    filter_by_currency
)

@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Пример транзакций для тестирования."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-02"},
        {"id": 3, "state": "PENDING", "date": "2023-01-03"},
        {"id": 4, "state": "EXECUTED", "date": "2023-01-04"},
    ]

class TestProcessing:
    def test_filter_by_state_executed(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Фильтрация по статусу EXECUTED."""
        filtered: List[Dict[str, Any]] = filter_by_state(
            sample_transactions, "EXECUTED"
        )
        assert len(filtered) == 3
        assert all(t["state"] == "EXECUTED" for t in filtered)

    def test_filter_by_state_not_found(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Фильтрация по несуществующему статусу."""
        filtered: List[Dict[str, Any]] = filter_by_state(
            sample_transactions, "CANCELLED"
        )
        assert len(filtered) == 0

    @pytest.mark.parametrize("sort_order,expected_first_id", [("asc", 1), ("desc", 4)])
    def test_sort_by_date(
        self,
        sample_transactions: List[Dict[str, Any]],
        sort_order: str,
        expected_first_id: int,
    ) -> None:
        """Сортировка по дате в разных направлениях."""
        sorted_transactions: List[Dict[str, Any]] = sort_by_date(
            sample_transactions, order=sort_order
        )
        assert sorted_transactions[0]["id"] == expected_first_id

    def test_sort_by_same_dates(self) -> None:
        """Сортировка при одинаковых датах."""
        transactions: List[Dict[str, Any]] = [
            {"id": 1, "date": "2023-01-01"},
            {"id": 2, "date": "2023-01-01"},
        ]
        sorted_transactions: List[Dict[str, Any]] = sort_by_date(
            transactions, order="asc"
        )
        assert sorted_transactions[0]["id"] == 1  # Порядок сохраняется

    def test_process_empty_list(self) -> None:
        """Тест обработки пустого списка транзакций."""
        result = process_transactions([])
        assert result == []

    def test_process_single_item(self) -> None:
        """Тест обработки одного элемента."""
        single_tx = {"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}
        result = process_transactions([single_tx])
        assert len(result) == 1

    def test_process_with_invalid_item(self) -> None:
        """Тест обработки списка с некорректным элементом."""
        invalid_tx = {"id": 1, "operationAmount": None}
        result = process_transactions([invalid_tx])
        assert result == []  # Некорректный элемент отфильтрован

    def test_filter_by_currency(self) -> None:
        """Тест фильтрации по валюте."""
        transactions = [
            {"operationAmount": {"currency": {"code": "RUB"}}},
            {"operationAmount": {"currency": {"code": "USD"}}}
        ]
        result = filter_by_currency(transactions, "RUB")
        assert len(result) == 1