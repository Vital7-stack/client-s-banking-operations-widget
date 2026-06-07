"""Модуль для маскирования номеров карт и счетов с логированием."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

# --- Настройка логгера (выполняется один раз при импорте модуля) ---
log_dir: Path = Path("logs")
log_dir.mkdir(exist_ok=True)

masks_logger: logging.Logger = logging.getLogger("masks")

# Чтобы не дублировать хендлеры при многократном импорте (частая проблема в тестах)
if not masks_logger.handlers:
    file_handler: logging.FileHandler = logging.FileHandler(log_dir / "masks.log", encoding="utf-8")
    formatter: logging.Formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    masks_logger.addHandler(file_handler)
    masks_logger.setLevel(logging.DEBUG)


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счёта, оставляя видимыми только последние 4 цифры.

    Правила:
      - Принимает только строку.
      - Удаляет пробелы и дефисы.
      - Длина очищенной строки должна быть >= 4.
      - Очищенная строка должна содержать только цифры.
      - Если итоговая маска имеет длину 4 (ровно 4 цифры) — возвращает "****".

    :param account_number: Номер счёта в виде строки.
    :return: Маскированный номер счёта.
    :raises TypeError: Если передан не str.
    :raises ValueError: Если номер слишком короткий или содержит нечисловые символы.
    """
    if not isinstance(account_number, str):
        masks_logger.error(
            "get_mask_account: некорректный тип данных: %s",
            type(account_number).__name__,
        )
        raise TypeError("Номер счёта должен быть строкой")

    cleaned: str = account_number.replace(" ", "").replace("-", "")

    if len(cleaned) < 4:
        masks_logger.error(
            "get_mask_account: номер счёта слишком короткий: %r (длина %d)",
            cleaned,
            len(cleaned),
        )
        raise ValueError("Номер счёта слишком короткий")

    if not cleaned.isdigit():
        masks_logger.error(
            "get_mask_account: номер счёта содержит нецифровые символы: %r",
            cleaned,
        )
        raise ValueError("Номер счёта должен содержать только цифры")

    masked: str = "*" * (len(cleaned) - 4) + cleaned[-4:]

    # Специальное правило: если маска ровно 4 символа — заменяем на 4 звёздочки
    if len(masked) == 4:
        masked = "****"

    masks_logger.debug(
        "get_mask_account(%r): %s",
        account_number,
        masked,
    )
    return masked


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты, оставляя видимыми первые 6 и последние 4 цифры.
    Формат вывода: XXXX **** **** XXXX (с пробелами).

    :param card_number: Номер карты в виде строки.
    :return: Отформатированный маскированный номер карты.
    :raises TypeError: Если передан не str.
    :raises ValueError: Если длина не 16 или есть нечисловые символы.
    """
    if not isinstance(card_number, str):
        masks_logger.error(
            "get_mask_card_number: некорректный тип данных: %s",
            type(card_number).__name__,
        )
        raise TypeError("Номер карты должен быть строкой")

    cleaned: str = card_number.replace(" ", "").replace("-", "")

    if len(cleaned) != 16:
        masks_logger.error(
            "get_mask_card_number: некорректная длина номера карты: %d",
            len(cleaned),
        )
        raise ValueError("Номер карты должен содержать 16 цифр")

    if not cleaned.isdigit():
        masks_logger.error(
            "get_mask_card_number: номер карты содержит нецифровые символы: %r",
            cleaned,
        )
        raise ValueError("Номер карты должен содержать только цифры")

    masked_core: str = cleaned[:6] + "*" * 6 + cleaned[-4:]
    formatted: str = f"{masked_core[:4]} {masked_core[4:8]} {masked_core[8:12]} {masked_core[12:]}"

    masks_logger.debug(
        "get_mask_card_number(%r): %s",
        card_number,
        formatted,
    )
    return formatted


def mask_account_card(input_number: Optional[str]) -> str:
    """
    Автоматически определяет тип номера (карта или счёт) и применяет
    соответствующую маску.

    Логика:
      - None, не-str или пустая строка → "invalid input"
      - Удаляются пробелы, дефисы и табуляции.
      - Если длина очищенной строки 16 и все цифры → маска карты + "(card)"
      - Если длина очищенной строки 20 и все цифры → маска счёта + "(account)"
      - В остальных случаях → "invalid input"

    :param input_number: Входной номер (может содержать разделители).
    :return: Маскированная строка с пометкой типа или "invalid input".
    """
    if input_number is None:
        return "invalid input"

    if not isinstance(input_number, str):
        masks_logger.error(
            "mask_account_card: некорректный тип данных: %s",
            type(input_number).__name__,
        )
        return "invalid input"

    if not input_number.strip():
        return "invalid input"

    # Очищаем все возможные разделители ДО вызова функций маскирования
    cleaned: str = input_number.replace(" ", "").replace("-", "").replace("\t", "")

    try:
        if len(cleaned) == 16 and cleaned.isdigit():
            masked: str = get_mask_card_number(cleaned)
            return f"{masked} (card)"

        if len(cleaned) == 20 and cleaned.isdigit():
            masked_account: str = get_mask_account(cleaned)
            return f"{masked_account} (account)"

        return "invalid input"
    except ValueError:
        # Перехватываем ошибки валидации из низкоуровневых функций
        return "invalid input"


def get_date(date_input: Optional[str]) -> str:
    """
    Преобразует дату в формат DD.MM.YYYY. Возвращает пустую строку при ошибке.

    Поддерживает форматы:
      - "YYYY-MM-DD"
      - "YYYY-MM-DDTHH:MM:SS" (отсекается время)

    :param date_input: Дата в виде строки или None.
    :return: Дата в формате DD.MM.YYYY или пустая строка.
    """
    if date_input is None:
        return ""

    date_str: str = str(date_input).strip()
    if not date_str:
        return ""

    try:
        date_part: str = date_str.split("T", 1)[0]
        dt: datetime = datetime.strptime(date_part, "%Y-%m-%d")
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        masks_logger.debug(
            "get_date: не удалось распарсить дату %r, возвращаем пустую строку",
            date_input,
        )
        return ""
