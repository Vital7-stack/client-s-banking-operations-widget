import json
import os

from logging_config import setup_logger

# Создаём логер для модуля utils
logger = setup_logger('utils')


def read_json_file(file_path):
    """Читает JSON‑файл и возвращает список транзакций или пустой список при ошибке."""
    try:
        if not os.path.exists(file_path):  # Если файла нет
            logger.warning(f"Файл не найден: {file_path}")
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.info(f"Успешно прочитан файл: {file_path}")

        if isinstance(data, list):  # Если данные — список
            return data
        else:  # Если данные не список
            logger.warning(f"Данные в файле {file_path} не являются списком")
            return []

    except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        return []

def some_utility_function():
    """Пример функции с логированием."""
    try:
        # Здесь может быть какая‑то логика
        logger.info("Функция some_utility_function успешно выполнена")
        # ... логика функции

    except Exception as e:
        logger.error(f"Ошибка в функции some_utility_function: {e}")
        raise

# Пример других функций в этом же файле (если есть)
def another_utility_function():
    """Ещё одна функция с использованием логера."""
    logger.debug("Вызвана функция another_utility_function")
    # ... логика функции
    logger.info("Функция another_utility_function завершена")


