import pytest  # noqa: F401
from typing import Any
from requests.exceptions import ConnectionError, Timeout

from src.external_api import convert_currency, fetch_operations


class TestConvertCurrency:
    def test_success(self, requests_mock: Any) -> None:
        requests_mock.get(
            "https://api.apilayer.com/exchangerates_data/latest",
            json={"rates": {"USD": 90.5}},
        )
        result = convert_currency(1000.0, "RUB", "USD")
        assert result == 90500.0

    def test_same_currency(self) -> None:
        assert convert_currency(123.456, "EUR", "EUR") == 123.46

    def test_no_api_key(self, monkeypatch: Any) -> None:
        monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "")
        result = convert_currency(100, "RUB", "USD")
        assert result == 0.0

    def test_request_exception(self, requests_mock: Any) -> None:
        requests_mock.get(
            "https://api.apilayer.com/exchangerates_data/latest",
            exc=Timeout,
        )
        result = convert_currency(100, "RUB", "USD")
        assert result == 0.0

    def test_rate_not_found(self, requests_mock: Any) -> None:
        requests_mock.get(
            "https://api.apilayer.com/exchangerates_data/latest",
            json={"rates": {}},
        )
        result = convert_currency(100, "RUB", "USD")
        assert result == 0.0


class TestFetchOperations:
    def test_network_error(self, requests_mock: Any) -> None:
        requests_mock.get(
            "https://api.bank.com",
            exc=ConnectionError,
        )
        result = fetch_operations("https://api.bank.com", "fake-token")
        assert result == []

    def test_timeout(self, requests_mock: Any) -> None:
        requests_mock.get(
            "https://api.bank.com",
            exc=Timeout,
        )
        result = fetch_operations("https://api.bank.com", "fake-token")
        assert result == []

    def test_returns_list_when_response_is_list(self, requests_mock: Any) -> None:
        data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
        requests_mock.get("https://api.bank.com", json=data)
        result = fetch_operations("https://api.bank.com", "fake-token")
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1

    def test_extracts_from_operations_key(self, requests_mock: Any) -> None:
        data = {
            "operations": [
                {"id": 3, "amount": 300},
                {"id": 4, "amount": 400},
            ],
            "meta": {"total": 2},
        }
        requests_mock.get("https://api.bank.com", json=data)
        result = fetch_operations("https://api.bank.com", "fake-token")
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 3

    def test_extracts_from_data_key(self, requests_mock: Any) -> None:
        data = {
            "data": [
                {"id": 5, "amount": 500},
                {"id": 6, "amount": 600},
            ]
        }
        requests_mock.get("https://api.bank.com", json=data)
        result = fetch_operations("https://api.bank.com", "fake-token")
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 5

    def test_unexpected_structure_returns_empty(self, requests_mock: Any) -> None:
        data = {"unknown_key": "value"}
        requests_mock.get("https://api.bank.com", json=data)
        result = fetch_operations("https://api.bank.com", "fake-token")
        assert result == []