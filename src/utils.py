import logging
from pathlib import Path
import json

# Создаём логгер для модуля utils
utils_logger = logging.getLogger('utils')
utils_logger.setLevel(logging.DEBUG)

# Настраиваем обработчик файла в папке logs в корне проекта
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)
log_file = log_dir / 'utils.log'

file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
utils_logger.addHandler(file_handler)

def calculate_sum(a, b):
    """Вычисляет сумму двух чисел."""
    # Отладочное логирование — фиксируем все вызовы
    utils_logger.debug(f"calculate_sum вызван с: a={a} (тип {type(a)}), b={b} (тип {type(b)})")

    try:
        # Проверка на None
        if a is None or b is None:
            utils_logger.error(f"calculate_sum: один из аргументов None: a={a}, b={b}")
            raise ValueError("Аргументы не должны быть None")

        # Проверка типов — должны быть числами
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            utils_logger.error(
                f"calculate_sum: некорректные типы: a={type(a)}, b={type(b)}"
            )
            raise TypeError("Оба аргумента должны быть числами (int или float)")

        result = a + b
        utils_logger.debug(f"calculate_sum({a}, {b}) = {result}")
        return result

    except Exception as e:
        utils_logger.error(f"Ошибка в calculate_sum: {e}")
        raise

def read_json_file(file_path):
    """Читает JSON-файл и возвращает данные.
    При ошибке возвращает пустой список.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            utils_logger.debug(f"read_json_file({file_path}): успешно прочитано {len(data)} элементов")
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        utils_logger.error(f"Ошибка чтения JSON-файла {file_path}: {e}")
        return []

def validate_data(data):
    """Валидирует данные.
    Возвращает True, если данные валидны.
    Вызывает ValueError, если данные невалидны.
    """
    try:
        if data is None:
            utils_logger.error("validate_data: данные не могут быть None")
            raise ValueError("Данные не могут быть None")
        if not isinstance(data, str):
            utils_logger.error("validate_data: данные должны быть строкой")
            raise ValueError("Данные должны быть строкой")
        if len(data.strip()) == 0:
            utils_logger.error("validate_data: данные не могут быть пустой строкой")
            raise ValueError("Данные не могут быть пустой строкой")

        utils_logger.debug("validate_data: данные успешно валидированы")
        return True
    except ValueError as e:
        utils_logger.error(f"validate_data: ошибка валидации: {e}")
        raise