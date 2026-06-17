from typing import Any, Dict, List
import json
import csv

from datetime import datetime
from src.processing import (
    filter_by_state,
    sort_by_date,
    process_bank_search,
)
from src.masks import mask_account_card

AVAILABLE_STATES = ["EXECUTED", "CANCELED", "PENDING"]


def load_transactions_from_json(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [{str(k): v for k, v in row.items()} for row in data]


def load_transactions_from_csv(path: str) -> List[Dict[str, Any]]:
    transactions = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append({str(k): v for k, v in row.items()})
    return transactions


def load_transactions_from_xlsx(path: str) -> List[Dict[str, Any]]:
    import pandas as pd
    df = pd.read_excel(path)
    records = df.to_dict(orient="records")
    return [{str(k): v for k, v in row.items()} for row in records]


def ask_yes_no(prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("да", "д", "yes", "y"):
            return True
        if answer in ("нет", "н", "no", "n"):
            return False
        print("Пожалуйста, ответьте «да» или «нет».")


def ask_sort_order() -> str:
    while True:
        answer = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        if "возр" in answer or answer == "asc":
            return "asc"
        if "убыв" in answer or answer == "desc":
            return "desc"
        print("Пожалуйста, введите «по возрастанию» или «по убыванию».")


def ask_state() -> str:
    while True:
        state = (
            input(
                "Введите статус, по которому необходимо выполнить фильтрацию.\n"
                "Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING\n"
            )
            .strip()
            .upper()
        )
        if state in AVAILABLE_STATES:
            return state
        print(f'Статус операции "{state}" недоступен.')
        print("Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING")


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")
    for t in transactions:
        date_raw = t.get("date", "")
        date_part = date_raw.split("T")[0] if isinstance(date_raw, str) else date_raw

        try:
            dt = datetime.strptime(str(date_part), "%Y-%m-%d")
            date_fmt = dt.strftime("%d.%m.%Y")
        except ValueError:
            date_fmt = str(date_part)

        description = t.get("description", "Без описания")
        amount = t.get("amount", "")
        currency = t.get("currency", "")

        from_acc = t.get("from_account", "")
        to_acc = t.get("to_account", "")

        from_masked = mask_account_card(from_acc) if from_acc else ""
        to_masked = mask_account_card(to_acc) if to_acc else ""

        print(date_fmt, description)
        if from_masked and to_masked:
            print(f"{from_masked} -> {to_masked}")
        elif from_masked:
            print(from_masked)
        elif to_masked:
            print("->", to_masked)

        if amount or currency:
            amount_str = f"{amount} {currency}" if currency else str(amount)
            print("Сумма:", amount_str)
        print()


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input().strip()
    path = input("Введите путь к файлу: ").strip()

    if choice not in ("1", "2", "3"):
        print("Неверный выбор пункта меню.")
        return

    try:
        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            transactions = load_transactions_from_json(path)
        elif choice == "2":
            print("Для обработки выбран CSV-файл.")
            transactions = load_transactions_from_csv(path)
        else:  # choice == "3"
            print("Для обработки выбран XLSX-файл.")
            transactions = load_transactions_from_xlsx(path)
    except FileNotFoundError:
        print("Ошибка: файл не найден. Проверьте путь.")
        return
    except PermissionError:
        print("Ошибка: нет прав на чтение файла.")
        return
    except json.JSONDecodeError as e:
        print(f"Ошибка в JSON-файле: {e}")
        return
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return

    state = ask_state()
    print(f'Операции отфильтрованы по статусу "{state}"')
    filtered = filter_by_state(transactions, state)

    if ask_yes_no("Отсортировать операции по дате? Да/Нет "):
        order = ask_sort_order()
        reverse = order == "desc"
        filtered = sort_by_date(filtered, reverse=reverse)

    if ask_yes_no("Выводить только рублевые транзакции? Да/Нет "):
        filtered = [t for t in filtered if t.get("currency") == "RUB"]

    if ask_yes_no("Отфильтровать список транзакций по определённому слову в описании? Да/Нет "):
        search_word = input("Введите слово для поиска: ").strip()
        filtered = process_bank_search(filtered, search_word)

    print("Распечатываю итоговый список транзакций...")
    print_transactions(filtered)
