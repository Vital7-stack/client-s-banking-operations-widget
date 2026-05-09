from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(
    transactions: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу."""
    if not transactions:
        return []
    return [t for t in transactions if t.get("state") == state]


def sort_by_date(
    transactions: List[Dict[str, Any]], order: str = "asc"
) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате."""
    if not transactions:
        return []

    def parse_date(date_str: str) -> datetime:
        """Парсит строку даты в объект datetime для корректного сравнения."""
        if "T" in date_str:
            date_part = date_str.split("T")[0]
        else:
            date_part = date_str
        try:
            return datetime.strptime(date_part, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Некорректный формат даты: {date_str}") from e

    # Сортируем по дате
    sorted_transactions = sorted(
        transactions, key=lambda x: parse_date(x["date"]), reverse=(order == "desc")
    )
    return sorted_transactions
