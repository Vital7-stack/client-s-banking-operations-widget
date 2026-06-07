from src.masks import (  # используем реальные имена
    get_mask_account,
    get_mask_card_number,
)
from src.utils import calculate_sum  # убираем несуществующую функцию

if __name__ == "__main__":
    # Тестируем логирование в utils
    calculate_sum(5, 3)  # оставляем существующую функцию

    # Тестируем логирование в masks
    result_card = get_mask_card_number("1234 5678 9012 3456")
    print(f"Маскированный номер карты: {result_card}")

    result_account = get_mask_account("12345678901234567890")
    print(f"Маскированный номер счёта: {result_account}")

    print("Проверьте файлы logs/utils.log и logs/masks.log")
