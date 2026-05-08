def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты по правилу 'XXXX XX** **** XXXX'.

    Args:
        card_number (str): Номер карты в виде строки.

    Returns:
        str: Замаскированный номер карты.
    """
    # Удаляем пробелы, если они есть
    cleaned_number = card_number.replace(" ", "")

    # Проверяем, что длина номера карты корректна (обычно 16 цифр)
    if len(cleaned_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Формируем маску: первые 6 цифр, затем 6 звёздочек, затем последние 4 цифры
    masked = f"{cleaned_number[:4]} {cleaned_number[4:6]}" f"** **** {cleaned_number[-4:]}"
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счёта по правилу '*XXXX'.

    Args:
        account_number (str): Номер счёта в виде строки.

    Returns:
        str: Замаскированный номер счёта.
    """
    # Удаляем пробелы, если они есть
    cleaned_number = account_number.replace(" ", "")

    # Проверяем, что номер счёта содержит хотя бы 4 цифры
    if len(cleaned_number) < 4:
        raise ValueError("Номер счёта должен содержать не менее 4 цифр")

    # Берём последние 4 цифры и добавляем две звёздочки перед ними
    return f"**{cleaned_number[-4:]}"
