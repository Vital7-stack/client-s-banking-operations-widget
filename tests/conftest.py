
from typing import Any, Dict, List

import pytest


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01T10:00:00", "description": "Перевод организации"},
        {"id": 2, "state": "PENDING", "date": "2023-01-02T11:00:00", "description": "Открытие вклада"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03T12:00:00", "description": "Перевод с карты на карту"},
        {"id": 4, "state": "FAILED", "date": "2023-01-04T13:00:00", "description": "Оплата услуг"},
    ]


@pytest.fixture
def card_numbers() -> Dict[str, str]:
    return {
        "valid_16": "1234567890123456",
        "short": "1234",
        "invalid": "abcdefghijklmnop",
        "with_spaces": "1234 5678 9012 3456",
    }


@pytest.fixture
def account_numbers() -> Dict[str, str]:
    return {
        "valid": "12345678901234567890",
        "short": "123",
        "with_spaces": "1234 5678 9012 3456 7890",
    }
