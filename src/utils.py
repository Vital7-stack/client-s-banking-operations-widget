import json
import os

def read_json_file(file_path):
    """Читает JSON‑файл и возвращает список транзакций или пустой список при ошибке."""
    try:
        if not os.path.exists(file_path):  # Если файла нет
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if isinstance(data, list):  # Если данные — список
            return data
        else:  # Если данные не список
            return []

    except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError):
        return []



