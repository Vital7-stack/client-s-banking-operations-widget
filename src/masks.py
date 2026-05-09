from typing import Optional


def get_mask_account(account_number: Optional[str]) -> str:
    """Маскирует номер счёта, заменяя все цифры на звёздочки, кроме последних 4 (если их больше 4)."""
    if account_number is None:
        return ""

    account_str: str = account_number.strip()

    if not account_str:
        return ""

    length: int = len(account_str)

    if length < 4:
        if length == 0:
            return ""
        elif length == 1:
            return account_str
        elif length == 2:
            return f"*{account_str[-1]}"
        else:  # length == 3
            return f"**{account_str[-1]}"
    elif length == 4:
        # Для длины 4 маскируем все цифры
        return "****"
    else:
        # Для длины > 4 маскируем всё, кроме последних 4 цифр
        return "*" * (length - 4) + account_str[-4:]


def get_mask_card_number(card_input: Optional[str]) -> str:
    """Маскирует номер карты, оставляя видимыми первые 4 и последние 4 цифры."""
    if card_input is None:
        return ""
    if not isinstance(card_input, str):
        return ""

    cleaned: str = card_input.replace(" ", "").replace("-", "")

    if len(cleaned) != 16 or not cleaned.isdigit():
        return ""

    formatted: str = f"{cleaned[:4]} {cleaned[4:8]}** **** {cleaned[-4:]}"
    return formatted


def mask_account_card(input_data: Optional[str]) -> str:
    """Распознаёт тип данных (карта/счёт) и возвращает маску с указанием типа."""
    if input_data is None:
        return "invalid input"
    if not isinstance(input_data, str):
        return "invalid input"

    cleaned: str = input_data.replace(" ", "").replace("-", "").replace("\t", "")

    if not cleaned.isdigit():
        return "invalid input"

    length: int = len(cleaned)

    masked: str
    account_type: str

    if length == 16:
        masked = get_mask_card_number(cleaned)
        account_type = "card"
    elif length >= 20:
        masked = get_mask_account(cleaned)
        account_type = "account"
    else:
        return "invalid input"

    return f"{masked} ({account_type})"
