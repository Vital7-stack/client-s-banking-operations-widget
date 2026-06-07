from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу."""
    return [tx for tx in transactions if tx.get("state") == state]


def sort_by_date(transactions: List[Dict[str, Any]], order: str = "asc") -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате."""
    sorted_transactions = sorted(transactions, key=lambda x: x.get("date", ""), reverse=(order == "desc"))
    return sorted_transactions


def process_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Обрабатывает список транзакций, фильтруя некорректные элементы."""
    if not transactions:
        return []
    result = []
    for tx in transactions:
        if tx.get("operationAmount") is not None:
            result.append(tx)
    return result


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по коду валюты."""
    filtered = []
    for tx in transactions:
        tx_currency = tx.get("operationAmount", {}).get("currency", {}).get("code")
        if tx_currency == currency_code:
            filtered.append(tx)
    return filtered
