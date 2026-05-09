from typing import List, Dict, Any

def filter_by_state(
    ops: List[Dict[str, Any]],
    state: str = 'EXECUTED'
) -> List[Dict[str, Any]]:
    """Фильтрует список операций по значению поля 'state'.

    Args:
        ops: Список словарей с данными о банковских операциях.
        state: Значение поля 'state' для фильтрации. По умолчанию 'EXECUTED'.

    Returns:
        Новый список словарей, где поле 'state' соответствует указанному значению.
    """
    return [op for op in ops if op.get('state') == state]

def print_operations(ops: List[Dict[str, Any]], status_name: str) -> None:
    """Выводит операции с указанным статусом."""
    print(f"Операции со статусом '{status_name}':")
    for op in ops:
        print(f"  ID: {op['id']}, Статус: {op['state']}, Дата: {op['date']}")

# Исходные данные: операции с разными статусами
operations: List[Dict[str, Any]] = [
    {
        'id': 41428829,
        'state': 'EXECUTED',
        'date': '2019-07-03T18:35:29.512364'
    },
    {
        'id': 939719570,
        'state': 'EXECUTED',
        'date': '2018-06-30T02:08:58.425572'
    },
    {
        'id': 594226727,
        'state': 'CANCELLED',
        'date': '2018-09-12T21:27:25.241689'
    }
]

# Пример 1: фильтрация по статусу по умолчанию ('EXECUTED')
executed_ops: List[Dict[str, Any]] = filter_by_state(operations)
print_operations(executed_ops, 'EXECUTED')

# Пример 2: фильтрация по другому статусу ('CANCELLED')
canceled_ops: List[Dict[str, Any]] = filter_by_state(operations, state='CANCELLED')
print_operations(canceled_ops, 'CANCELLED')