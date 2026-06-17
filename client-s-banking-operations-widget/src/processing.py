from collections import Counter
from typing import List, Dict, Any


def filter_by_status(
    transactions: List[Dict[str, Any]], status: str
) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу. Поддерживает ключи 'state' и 'status'."""
    result = []
    for t in transactions:
        t_state = t.get("state") or t.get("status")
        if t_state == status:
            result.append(t)
    return result


def sort_by_date(
    transactions: List[Dict[str, Any]], ascending: bool = True
) -> List[Dict[str, Any]]:
    """Сортирует транзакции по полю 'date'. Если даты нет — такие транзакции идут в конец."""

    def get_date_key(t: Dict[str, Any]) -> str:
        return t.get("date", "") or ""

    return sorted(transactions, key=get_date_key, reverse=not ascending)


def count_operations_by_category(transactions: List[Dict[str, Any]]) -> Counter:
    """Подсчитывает количество операций по полю 'category'. Возвращает пустой Counter, если категорий нет."""
    categories = [t.get("category") for t in transactions if t.get("category")]
    return Counter(categories)
