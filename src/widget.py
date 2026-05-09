from datetime import datetime
from typing import Union


def mask_account_card(input_data: Union[str, None]) -> str:
    """Распознаёт тип данных (карта/счёт) и возвращает маску с указанием типа."""
    if input_data is None or not str(input_data).strip():
        return "invalid input"

    cleaned: str = str(input_data).replace(" ", "").replace("-", "").replace("\t", "")

    # Проверка на цифры
    if not cleaned.isdigit():
        return "invalid input"

    length: int = len(cleaned)

    if length == 16:
        return f"{cleaned[:4]} {cleaned[4:6]}** **** {cleaned[-4:]} (card)"
    elif length >= 20:
        return f"{'*' * (length - 4)}{cleaned[-4:]} (account)"
    else:
        return "invalid input"


def get_date(date_input: Union[str, None]) -> str:
    """Преобразует дату в формат DD.MM.YYYY."""
    if date_input is None or not str(date_input).strip():
        return ""

    date_str: str = str(date_input).strip()

    try:
        # Извлекаем часть с датой (до T, если есть)
        date_part: str = date_str.split("T")[0] if "T" in date_str else date_str
        dt: datetime = datetime.strptime(date_part, "%Y-%m-%d")
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        return ""
