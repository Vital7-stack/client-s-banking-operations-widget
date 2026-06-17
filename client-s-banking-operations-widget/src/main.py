from typing import List, Dict, Any
from src.processing import filter_by_status, sort_by_date, count_operations_by_category
from src.utils import (
    load_transactions_from_json,
    load_transactions_from_csv,
    load_transactions_from_xlsx,
)


def ask_yes_no(prompt: str) -> bool:
    """Спрашивает пользователя «да/нет», возвращает True/False."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("да", "д", "yes", "y"):
            return True
        if answer in ("нет", "н", "no", "n"):
            return False
        print("Пожалуйста, введите «да» или «нет».")


def main() -> None:
    print("Выберите тип файла для обработки:")
    print("1. JSON")
    print("2. CSV")
    print("3. XLSX")

    file_type = input("Введите номер: ").strip()
    path = input("Введите путь к файлу: ").strip()

    transactions: List[Dict[str, Any]] = []

    # --- Блок загрузки с обработкой ошибок ---
    try:
        if file_type == "1":
            transactions = load_transactions_from_json(path)
        elif file_type == "2":
            transactions = load_transactions_from_csv(path)
        elif file_type == "3":
            transactions = load_transactions_from_xlsx(path)
        else:
            print("Неверный тип файла.")
            return
    except FileNotFoundError:
        print(f"Ошибка: файл не найден — {path}")
        return
    except ValueError as e:
        # Сюда попадёт, например, неверный JSON
        print(f"Ошибка при чтении файла: {e}")
        return
    except Exception as e:
        # Любой другой сбой (например, битый XLSX)
        print(f"Произошла ошибка при обработке файла: {e}")
        return

    if not transactions:
        print("Транзакции не найдены.")
        return

    status = input(
        "Введите статус для фильтрации (или оставьте пустым для всех): "
    ).strip()
    if status:
        transactions = filter_by_status(transactions, status)
        print(f'Операции отфильтрованы по статусу "{status}"')

    sort_order = (
        input("Сортировать по дате (по возрастанию/по убыванию/пусто): ")
        .strip()
        .lower()
    )
    ascending = True
    if sort_order == "по убыванию":
        ascending = False
    elif sort_order not in ("", "по возрастанию"):
        print("Неверная сортировка, используется по возрастанию.")

    transactions = sort_by_date(transactions, ascending=ascending)

    currency = (
        input("Только операции в валюте (оставьте пустым для всех): ").strip().upper()
    )
    if currency:
        transactions = [t for t in transactions if t.get("currency_code") == currency]
        print(f"Отфильтровано по валюте: {currency}")

    search_text = input("Поиск по описанию (оставьте пустым, если не нужно): ").strip()
    if search_text:
        transactions = [
            t
            for t in transactions
            if search_text.lower() in str(t.get("description", "")).lower()
        ]
        print(f"Найдено по описанию: {len(transactions)} операций")

    if ask_yes_no("Показать статистику по категориям? Да/Нет "):
        counter = count_operations_by_category(transactions)
        print("Статистика по категориям:")
        for category, count in counter.most_common():
            print(f"{category}: {count}")

    print(f"\nВсего отобрано операций: {len(transactions)}")
