from typing import Optional
import logging

# Настройка логера (если нет отдельного модуля logging_config)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('masks')


def get_mask_account(account_number: Optional[str]) -> str:
    """Маскирует номер счёта, заменяя все цифры на звёздочки, кроме последних 4 (если их больше 4)."""
    if account_number is None:
        logger.warning("Получен None вместо номера счёта")
        return ""

    account_str: str = account_number.strip()

    if not account_str:
        logger.warning("Получена пустая строка или строка с пробелами вместо номера счёта")
        return ""

    length: int = len(account_str)

    if length < 4:
        if length == 0:
            return ""
        elif length == 1:
            logger.info("Номер счёта из 1 цифры — возвращается без маскировки")
            return account_str
        elif length == 2:
            logger.info("Номер счёта из 2 цифр — маскируется первая цифра")
            return f"*{account_str[-1]}"
        else:  # length == 3
            logger.info("Номер счёта из 3 цифр — маскируются первые две цифры")
            return f"**{account_str[-1]}"
    elif length == 4:
        # Для длины 4 маскируем все цифры
        logger.info("Номер счёта из 4 цифр — все цифры маскируются")
        return "****"
    else:
        # Для длины > 4 маскируем всё, кроме последних 4 цифр
        logger.info(f"Номер счёта длиной {length} — маскируются все цифры, кроме последних 4")
        return "*" * (length - 4) + account_str[-4:]



def get_mask_card_number(card_input: Optional[str]) -> str:
    """Маскирует номер карты, оставляя видимыми первые 4 и последние 4 цифры."""
    if card_input is None:
        logger.warning("Получен None вместо номера карты")
        return ""
    if not isinstance(card_input, str):
        logger.error(f"Некорректный тип данных для номера карты: {type(card_input)}")
        return ""

    cleaned: str = card_input.replace(" ", "").replace("-", "")

    if len(cleaned) != 16 or not cleaned.isdigit():
        logger.error(f"Некорректный номер карты: {card_input} (очищенный: {cleaned})")
        return ""

    formatted: str = f"{cleaned[:4]} {cleaned[4:8]}** **** {cleaned[-4:]}"
    logger.info(f"Номер карты успешно замаскирован: {formatted}")
    return formatted



def mask_account_card(input_data: Optional[str]) -> str:
    """Распознаёт тип данных (карта/счёт) и возвращает маску с указанием типа."""
    if input_data is None:
        logger.warning("Получен None в качестве входных данных")
        return "invalid input"
    if not isinstance(input_data, str):
        logger.error(f"Некорректный тип входных данных: {type(input_data)}")
        return "invalid input"

    cleaned: str = input_data.replace(" ", "").replace("-", "").replace("\t", "")

    if not cleaned.isdigit():
        logger.error(f"Входные данные содержат нецифровые символы: {input_data}")
        return "invalid input"

    length: int = len(cleaned)

    masked: str
    account_type: str

    if length == 16:
        masked = get_mask_card_number(cleaned)
        account_type = "card"
        logger.info("Обнаружен номер карты (16 цифр)")
    elif length >= 20:
        masked = get_mask_account(cleaned)
        account_type = "account"
        logger.info(f"Обнаружен номер счёта (длина {length} цифр)")
    else:
        logger.warning(f"Неподдерживаемая длина данных: {length}")
        return "invalid input"

    result = f"{masked} ({account_type})"
    logger.info(f"Результат маскировки: {result}")
    return result



def apply_mask(input_data: Optional[str]) -> str:
    """
    Основная функция для применения маскировки к входным данным.
    Возвращает замаскированную строку с указанием типа (карта/счёт) или сообщение об ошибке.
    """
    try:
        result = mask_account_card(input_data)
        if result != "invalid input":
            logger.info("Маска успешно применена")
        else:
            logger.warning("Не удалось применить маску — некорректные входные данные")
        return result
    except Exception as e:
        logger.error(f"Критическая ошибка при применении маски: {e}")
        return "error during masking"

# Примеры использования
if __name__ == "__main__":
    # Тестовые случаи
    print(apply_mask("1234567890123456"))  # Карта
    print(apply_mask("40702810500000012345"))  # Счёт
    print(apply_mask("123"))  # Некорректные данные
    print(apply_mask(None))  # None
    print(apply_mask("12 34 56 78 90 12 34 56"))  # Карта с пробелами
    print(apply_mask("4070-2810-5000-0001-2345"))  # Счёт с дефисами
