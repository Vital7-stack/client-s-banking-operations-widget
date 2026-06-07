from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


def _normalize_record(record: Dict[Any, Any]) -> Dict[str, Any]:
    """Приводит все ключи словаря к строкам (на случай, если pandas вернёт не str)."""
    return {str(key): value for key, value in record.items()}


def read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV-файл не найден: {file_path}")
    if not path.is_file():
        raise ValueError(f"Указанный путь не является файлом: {file_path}")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("CSV-файл пуст: нет данных для обработки.")

    # to_dict возвращает dict с Hashable-ключами; нормализуем их к str
    raw_records = df.to_dict(orient="records")
    return [_normalize_record(record) for record in raw_records]


def read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Excel-файл не найден: {file_path}")
    if not path.is_file():
        raise ValueError(f"Указанный путь не является файлом: {file_path}")

    try:
        df = pd.read_excel(path, engine="openpyxl")
    except Exception as e:
        # Пробрасываем понятную ошибку, сохраняя оригинал через `from e`
        raise RuntimeError(f"Не удалось прочитать Excel-файл: {path}") from e

    if df.empty:
        raise ValueError("Excel-лист пуст: нет данных для обработки.")

    raw_records = df.to_dict(orient="records")
    return [_normalize_record(record) for record in raw_records]
