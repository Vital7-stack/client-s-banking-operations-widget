import logging
import os


def setup_logger(module_name: str) -> logging.Logger:
    """
    Создаёт и настраивает логер для указанного модуля.

    Args:
        module_name (str): имя модуля (например, 'utils' или 'masks')

    Returns:
        logging.Logger: настроенный объект логера
    """
    # Создаём логер с именем модуля
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования не ниже DEBUG

    # Очищаем существующие handler'ы, чтобы избежать дублирования
    logger.handlers.clear()

    # Форматирование логов: время, модуль, уровень, сообщение
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Путь к файлу лога
    log_file_path = os.path.join('logs', f'{module_name}.log')

    # FileHandler с режимом 'w' — перезаписывает файл при каждом запуске
    file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)

    # Добавляем handler к логеру
    logger.addHandler(file_handler)

    return logger