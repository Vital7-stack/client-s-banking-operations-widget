import logging
from pathlib import Path
from typing import Any

def setup_logger(
    name: str,
    log_file: str = 'logs/masks.log',
    level: int = logging.DEBUG
) -> logging.Logger:
    """Настраивает логгер с записью в файл и консоль."""
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)


    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S,%f'
    )

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def calculate_sum(a_input: Any, b_input: Any, logger: logging.Logger) -> str:
    """
    Безопасное сложение двух значений с преобразованием в строки.

    Args:
        a_input: Первое значение (может быть любого типа)
        b_input: Второе значение (может быть любого типа)
        logger: Объект логгера для записи сообщений

    Returns:
        str: Конкатенированная строка из двух преобразованных значений
    """
    # Преобразуем входные значения в строки, заменяя None на пустую строку
    a_str = str(a_input) if a_input is not None else ""
    b_str = str(b_input) if b_input is not None else ""

    try:
        # Вычисляем результат внутри блока try
        concatenated_result = a_str + b_str
        # Логируем отладочную информацию
        logger.debug(f"calculate_sum({repr(a_input)}, {repr(b_input)}) = {concatenated_result}")
        return concatenated_result
    except Exception as exc:
        # Используем другое имя для исключения
        logger.error(
            f"Ошибка в calculate_sum: {exc}. "
            f"a={repr(a_input)} (тип: {type(a_input).__name__}), "
            f"b={repr(b_input)} (тип: {type(b_input).__name__})"
        )
        raise

# Настройка глобального логгера
main_logger = setup_logger('utils', 'logs/app.log')

if __name__ == "__main__":
    print("=== Тестирование функции calculate_sum ===")

    tests = [
        ('Сумма: ', 100),
        (None, 'текст'),
        ('текст', None),
        (None, None),
        (123, 456),
        ('', ''),
        ('Число: ', 42.5),
    ]

    for test_a, test_b in tests:
        try:
            result_value = calculate_sum(test_a, test_b, main_logger)
            print(f"calculate_sum({test_a!r}, {test_b!r}) = {result_value}")
        except Exception as error_exc:
            print(f"Ошибка с параметрами {test_a!r}, {test_b!r}: {error_exc}")

    print("\n=== Проверьте файл logs/app.log для просмотра логов ===")