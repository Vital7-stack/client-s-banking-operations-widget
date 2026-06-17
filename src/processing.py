
import re
from typing import List, Dict, Any


def filter_by_state(transactions: List[Dict[str, Any]], state: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу (регистронезависимо).
    :param transactions: список словарей транзакций
    :param state: статус для фильтрации (EXECUTED, CANCELED, PENDING)
    :return: отфильтрованный список транзакций
    """
    target = state.upper()
    return [t for t in transactions if t.get("state", "").upper() == target]


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате (по возрастанию или убыванию).
    :param transactions: список транзакций
    :param reverse: если True — сортировка по убыванию
    :return: отсортированный список транзакций
    """
    def parse_date(t: Dict[str, Any]) -> str:
        d = t.get("date", "")
        if isinstance(d, str):
            # берем только дату до T
            return d.split("T")[0]
        return str(d)

    return sorted(transactions, key=parse_date, reverse=reverse)


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по подстроке в описании с использованием регулярных выражений.
    Поиск регистронезависимый.
    :param data: список словарей с транзакциями
    :param search: строка поиска (подстрока)
    :return: список найденных транзакций
    """
    if not search:
        return data
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [t for t in data if pattern.search(str(t.get("description", "")))]


def process_bank_operations(
    data: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям (по полю description).
    Для подсчёта используется Counter.
    :param data: список транзакций
    :param categories: список категорий (подстрок) для поиска в description
    :return: словарь {категория: количество}
    """
    result = {}
    for cat in categories:
        pattern = re.compile(re.escape(cat), re.IGNORECASE)
        count = sum(1 for t in data if pattern.search(str(t.get("description", ""))))
        result[cat] = count
    return result
