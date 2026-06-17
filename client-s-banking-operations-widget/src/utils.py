import csv
import json
import pandas as pd
from typing import List, Dict, Any


def load_transactions_from_json(path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if isinstance(data, list):
        return data  # type: ignore[return-value]

    if isinstance(data, dict):
        if "operations" in data and isinstance(data["operations"], list):
            return data["operations"]  # type: ignore[return-value]
        if "data" in data and isinstance(data["data"], list):
            return data["data"]  # type: ignore[return-value]

    return []


def load_transactions_from_csv(path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из CSV-файла.
    Поддерживает CSV как с заголовком, так и без него.
    Разделитель — точка с запятой (;).
    Пропускает строки, где нет state/date или amount не является числом.
    """
    transactions: List[Dict[str, Any]] = []
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            first_line = f.readline().strip()
            f.seek(0)

            has_header = first_line.lower().startswith(
                ("id,", "id;", "state,", "state;", "date,", "date;")
            )

            if has_header:
                if ";" in first_line and "," not in first_line:
                    reader = csv.DictReader(f, delimiter=";")
                else:
                    reader = csv.DictReader(f, delimiter=",")
            else:
                fieldnames = [
                    "id",
                    "state",
                    "date",
                    "amount",
                    "currency_name",
                    "currency_code",
                    "from",
                    "to",
                    "description",
                ]
                reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=";")

            for row in reader:
                # Валидация обязательных полей
                if not row.get("state") or not row.get("date"):
                    continue

                # Валидация amount
                try:
                    amount = float(row["amount"])
                except (ValueError, TypeError):
                    continue

                transactions.append(
                    {
                        "id": row.get("id"),
                        "state": row["state"],
                        "date": row["date"],
                        "amount": amount,
                        "currency_name": row.get("currency_name"),
                        "currency_code": row.get("currency_code"),
                        "from": row.get("from"),
                        "to": row.get("to"),
                        "description": row.get("description"),
                    }
                )
    except FileNotFoundError:
        return []
    except Exception:
        # На случай любых других проблем с файлом
        return []

    return transactions


def load_transactions_from_xlsx(path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из XLSX-файла через pandas."""
    try:
        df = pd.read_excel(path)
        records = df.to_dict(orient="records")
        return records  # type: ignore[return-value]
    except ImportError:
        # Если нет библиотеки openpyxl
        return []
    except Exception:
        # Любая другая ошибка (битый файл, неверный формат)
        return []
