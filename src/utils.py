import json
import logging
from pathlib import Path
from typing import Any, cast

utils_logger = logging.getLogger("utils")


def init_utils_logging(log_dir: str = "logs") -> None:
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    file_handler = logging.FileHandler(
        log_path / "utils.log",
        mode="a",
        encoding="utf-8",
    )
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    if not any(isinstance(h, logging.FileHandler) for h in utils_logger.handlers):
        utils_logger.addHandler(file_handler)

    utils_logger.setLevel(logging.DEBUG)


def calculate_sum(a: Any, b: Any) -> float:
    utils_logger.debug(f"calculate_sum вызван с: a={a} (тип {type(a)}), b={b} (тип {type(b)})")

    if a is None or b is None:
        msg = "Аргументы не должны быть None"
        utils_logger.error(f"calculate_sum: {msg} — a={a}, b={b}")
        raise ValueError(msg)

    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        msg = "Оба аргумента должны быть числами (int или float)"
        utils_logger.error(f"calculate_sum: {msg} — a={type(a)}, b={type(b)}")
        raise TypeError(msg)

    result = a + b
    utils_logger.debug(f"calculate_sum({a}, {b}) = {result}")
    return float(result)


def read_json_file(file_path: str) -> list | dict:
    """Читает JSON-файл и возвращает данные. При ошибке возвращает пустой список."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
            # Явно приводим тип: mypy понимает, что мы обещаем list | dict
            data = cast(list | dict, raw)

        count = len(data) if isinstance(data, (list, dict)) else 0
        utils_logger.debug(f"read_json_file({file_path}): успешно прочитано {count} элементов")
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        utils_logger.error(f"Ошибка чтения JSON-файла {file_path}: {e}")
        return []


def validate_data(data: Any) -> bool:
    if data is None:
        msg = "Данные не могут быть None"
        utils_logger.error(f"validate_data: {msg}")
        raise ValueError(msg)

    if not isinstance(data, str):
        msg = "Данные должны быть строкой"
        utils_logger.error(f"validate_data: {msg}")
        raise ValueError(msg)

    if len(data.strip()) == 0:
        msg = "Данные не могут быть пустой строкой"
        utils_logger.error(f"validate_data: {msg}")
        raise ValueError(msg)

    utils_logger.debug("validate_data: данные успешно валидированы")
    return True


def convert_currency(amount: Any, rate: Any) -> float:
    if amount is None or rate is None:
        msg = "Аргументы не должны быть None"
        utils_logger.error(f"convert_currency: {msg}")
        raise ValueError(msg)

    if not isinstance(amount, (int, float)) or not isinstance(rate, (int, float)):
        msg = "Оба аргумента должны быть числами (int или float)"
        utils_logger.error(f"convert_currency: {msg}")
        raise TypeError(msg)

    result = float(amount * rate)
    utils_logger.debug(f"convert_currency({amount}, {rate}) = {result}")
    return result
