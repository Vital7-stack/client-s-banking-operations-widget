from typing import Any, Dict, Generator, List


def filter_by_currency(
    transactions: List[Dict[str, Any]], currency: str
) -> Generator[Dict[str, Any], None, None]:
    """
    Фильтр транзакций по валюте.

    Args:
        transactions: список транзакций
        currency: код валюты для фильтрации

    Yields:
        Транзакции с указанной валютой
    """
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(
    transactions: List[Dict[str, Any]],
) -> Generator[str, None, None]:
    """
    Генератор описаний транзакций.

    Args:
        transactions: список транзакций

    Yields:
        Описания транзакций
    """
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Генератор номеров карт в формате 'XXXX XXXX XXXX XXXX'.

    Args:
        start: начальное число (включительно)
        stop: конечное число (не включительно)

    Yields:
        Строка с номером карты в формате с пробелами каждые 4 цифры
    """
    for num in range(start, stop):
        # Преобразуем число в строку и дополняем нулями до 16 цифр
        num_str = str(num).zfill(16)
        # Разбиваем на блоки по 4 символа
        formatted = " ".join(num_str[i : i + 4] for i in range(0, 16, 4))
        yield formatted
