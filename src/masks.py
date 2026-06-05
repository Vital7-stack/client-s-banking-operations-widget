import logging
from pathlib import Path

# Настройка логирования
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)
masks_logger = logging.getLogger('masks')
file_handler = logging.FileHandler(log_dir / 'masks.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
masks_logger.addHandler(file_handler)
masks_logger.setLevel(logging.DEBUG)


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счёта, оставляя видимыми только последние 4 цифры."""
    if not isinstance(account_number, str):
        masks_logger.error(f"get_mask_account: некорректный тип данных: {type(account_number)}")
        raise TypeError("Номер счёта должен быть строкой")

    # Удаляем пробелы и дефисы
    cleaned = account_number.replace(' ', '').replace('-', '')

    if len(cleaned) < 4:
        masks_logger.error(f"get_mask_account: номер счёта слишком короткий: {cleaned}")
        raise ValueError("Номер счёта слишком короткий")

    if not cleaned.isdigit():
        masks_logger.error(f"get_mask_account: номер счёта содержит нецифровые символы: {cleaned}")
        raise ValueError("Номер счёта должен содержать только цифры")

    # Всегда маскируем все цифры, кроме последних 4
    masked = '*' * (len(cleaned) - 4) + cleaned[-4:]

    # СПЕЦИАЛЬНОЕ ПРАВИЛО: если длина маски равна 4 (ровно 4 цифры), заменяем на 4 звёздочки
    if len(masked) == 4:
        masked = '****'

    masks_logger.debug(f"get_mask_account({account_number}): {masked}")
    return masked

def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты, оставляя видимыми первые 6 и последние 4 цифры."""
    if not isinstance(card_number, str):
        masks_logger.error(f"get_mask_card_number: некорректный тип данных: {type(card_number)}")
        raise TypeError("Номер карты должен быть строкой")

    # Удаляем пробелы и дефисы
    cleaned = card_number.replace(' ', '').replace('-', '')

    if len(cleaned) != 16:
        masks_logger.error(f"get_mask_card_number: некорректная длина номера карты: {len(cleaned)}")
        raise ValueError("Номер карты должен содержать 16 цифр")

    if not cleaned.isdigit():
        masks_logger.error(f"get_mask_card_number: номер карты содержит нецифровые символы: {cleaned}")
        raise ValueError("Номер карты должен содержать только цифры")

    masked = cleaned[:6] + '*' * 6 + cleaned[-4:]
    # Форматируем с пробелами: 1234 56** **** 3456
    formatted = f"{masked[:4]} {masked[4:8]} {masked[8:12]} {masked[12:]}"
    masks_logger.debug(f"get_mask_card_number({card_number}): {formatted}")
    return formatted

def mask_account_card(input_number: str | None) -> str:
    """Автоматически определяет тип номера (карта или счёт) и применяет соответствующую маску."""
    # Обработка None
    if input_number is None:
        return "invalid input"

    if not isinstance(input_number, str):
        masks_logger.error(f"mask_account_card: некорректный тип данных: {type(input_number)}")
        return "invalid input"

    if not input_number:
        return "invalid input"

    # Очищаем от пробелов и дефисов
    cleaned = input_number.replace(' ', '').replace('-', '')

    if len(cleaned) == 16 and cleaned.isdigit():
        try:
            masked = get_mask_card_number(input_number)
            return f"{masked} (card)"
        except ValueError:
            return "invalid input"
    elif len(cleaned) == 20 and cleaned.isdigit():
        try:
            masked = get_mask_account(input_number)
            return f"{masked} (account)"
        except ValueError:
            return "invalid input"
    else:
        return "invalid input"