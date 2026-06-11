from typing import Optional


def get_mask_account(account_number: Optional[str]) -> str:
    """Маскирует номер счёта, заменяя все цифры на звёздочки, кроме последних 4."""
    if account_number is None:
        return ""

    account_str: str = str(account_number).strip()
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

    if length == 4:
        return "****"

    return "*" * (length - 4) + account_str[-4:]


def get_mask_card_number(card_input: Optional[str]) -> str:
    """Маскирует номер карты, оставляя видимыми первые 4 и последние 4 цифры."""
    if card_input is None or not isinstance(card_input, str):
        return ""

    cleaned: str = card_input.replace(" ", "").replace("-", "").replace("\t", "")
    if len(cleaned) != 16 or not cleaned.isdigit():
        return ""

    formatted: str = f"{cleaned[:4]} {cleaned[4:8]}** **** {cleaned[-4:]}"
    return formatted


def mask_account_card(input_data: Optional[str]) -> str:
    """
    Распознаёт тип данных (карта/счёт) и возвращает маску с указанием типа.

    Правила:
      - 16 цифр → карта
      - >= 20 цифр → счёт
      - иначе → invalid input
    """
    if input_data is None or not isinstance(input_data, str):
        return "invalid input"

    cleaned: str = input_data.replace(" ", "").replace("-", "").replace("\t", "")
    if not cleaned.isdigit():
        return "invalid input"

    length: int = len(cleaned)

    if length == 16:
        masked: str = get_mask_card_number(cleaned)
        return f"{masked} (card)"

    if length >= 20:
        masked = get_mask_account(cleaned)
        return f"{masked} (account)"

    return "invalid input"
