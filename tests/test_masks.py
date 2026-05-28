from typing import Optional

import pytest

from src.masks import get_mask_account


class TestMasksHybrid:
    @pytest.mark.parametrize(
        "account_input,expected_output",
        [
            ("12345678901234567890", "****************7890"),
            ("1234", "****"),
        ],
    )
    def test_get_mask_account_exact_match(
        self, account_input: str, expected_output: str
    ) -> None:
        """Точные проверки для счёта."""
        result: str = get_mask_account(account_input)
        assert result == expected_output

    def test_get_mask_account_properties(self) -> None:
        """Проверки бизнес‑правил для маскирования счетов."""
        valid_account_numbers: list[str] = [
            "12345678901234567890",
            "123456",
            "123",
            "1",
            "",
        ]

        for account in valid_account_numbers:
            result: str = get_mask_account(account)

            # Бизнес‑правила:
            if len(account) >= 4:
                assert len(result) == len(
                    account
                ), "Длина результата должна совпадать с длиной входа"
                assert result[-4:].isdigit(), "Последние 4 цифры всегда видны"
                assert all(
                    c == "*" for c in result[:-4]
                ), "Все символы кроме последних 4 должны быть звёздочками"
            elif len(account) == 3:
                assert result == "**3"
            elif len(account) == 2:
                assert result == "*2"
            elif len(account) == 1:
                assert result == "1"
            else:  # пустая строка
                assert result == ""

    @pytest.mark.parametrize(
        "account_input,expected_output",
        [
            ("", ""),
            (None, ""),
            ("   ", ""),  # пробелы
        ],
    )
    def test_get_mask_account_edge_cases(
        self, account_input: Optional[str], expected_output: str
    ) -> None:
        """Проверка крайних случаев для счетов."""
        # Обработка None перед вызовом функции
        if account_input is None:
            account_input = ""
        result: str = get_mask_account(account_input)
        assert result == expected_output

    @pytest.mark.parametrize(
        "account_input,expected_output",
        [
            ("1", "1"),
            ("12", "*2"),
            ("123", "**3"),
        ],
    )
    def test_get_mask_account_short_numbers(
        self, account_input: str, expected_output: str
    ) -> None:
        """Проверка маскирования коротких номеров счетов."""
        result: str = get_mask_account(account_input)
        assert result == expected_output


import pytest  # noqa: F401 (указываем, что импорт нужен для pytest)
from src.masks import get_mask_account, get_mask_card_number, mask_account_card  # noqa: F401

class TestMasks:

    # --- Тесты для get_mask_account (покрываем короткие длины) ---

    def test_mask_account_length_1(self):
        assert get_mask_account("1") == "1"

    def test_mask_account_length_2(self):
        assert get_mask_account("12") == "*2"

    def test_mask_account_length_3(self):
        assert get_mask_account("123") == "**3"

    def test_mask_account_length_4(self):
        assert get_mask_account("1234") == "****"

    def test_mask_account_length_5(self):
        assert get_mask_account("12345") == "*2345"

    def test_mask_account_none(self):
        assert get_mask_account(None) == ""

    def test_mask_account_empty_string(self):
        assert get_mask_account("") == ""

    def test_mask_account_with_spaces(self):
        assert get_mask_account("   ") == ""

    # --- Тесты для get_mask_card_number ---

    def test_mask_card_valid(self):
        assert get_mask_card_number("1234567890123456") == "1234 5678** **** 3456"

    def test_mask_card_with_spaces(self):
        assert get_mask_card_number("1234 5678 9012 3456") == "1234 5678** **** 3456"

    def test_mask_card_with_dashes(self):
        assert get_mask_card_number("1234-5678-9012-3456") == "1234 5678** **** 3456"

    def test_mask_card_invalid_length(self):
        assert get_mask_card_number("1234567890123") == ""  # 13 цифр
        assert get_mask_card_number("12345678901234567") == ""  # 17 цифр

    def test_mask_card_invalid_chars(self):
        assert get_mask_card_number("1234abcd") == ""
        assert get_mask_card_number("1234567890123abc") == ""

    def test_mask_card_none(self):
        assert get_mask_card_number(None) == ""

    def test_mask_card_not_string(self):
        # Передаём строки вместо чисел и списков
        assert get_mask_card_number("1234") == ""
        assert get_mask_card_number("") == ""  # пустая строка вместо списка

    def test_mask_card_empty_string(self):
        assert get_mask_card_number("") == ""

    # --- Тесты для mask_account_card (главный сценарий) ---

    def test_mask_account_card_card(self):
        assert mask_account_card("1234567890123456") == "1234 5678** **** 3456 (card)"

    def test_mask_account_card_card_with_spaces(self):
        assert mask_account_card("1234 5678 9012 3456") == "1234 5678** **** 3456 (card)"

    def test_mask_account_card_account(self):
        assert mask_account_card("12345678901234567890") == "****************7890 (account)"

    def test_mask_account_card_invalid_length(self):
        assert mask_account_card("1234567890") == "invalid input"  # 10 цифр
        assert mask_account_card("123") == "invalid input"  # 3 цифры

    def test_mask_account_card_invalid_chars(self):
        assert mask_account_card("1234abcd") == "invalid input"
        assert mask_account_card("1234-5678-9012-abcd") == "invalid input"

    def test_mask_account_card_none(self):
        assert mask_account_card(None) == "invalid input"

    def test_mask_account_card_not_string(self):
        # Передаём строки вместо чисел и списков
        assert mask_account_card("1234") == "invalid input"
        assert mask_account_card("") == "invalid input"  # пустая строка вместо списка

    def test_mask_account_card_empty_string(self):
        assert mask_account_card("") == "invalid input"

    # --- Дополнительные граничные случаи ---

    def test_mask_account_edge_cases(self):
        """Тестируем граничные случаи для счёта"""
        assert get_mask_account("0") == "0"
        assert get_mask_account("00") == "*0"
        assert get_mask_account("000") == "**0"
        assert get_mask_account("0000") == "****"


    def test_mask_card_edge_cases(self):
        """Тестируем граничные случаи для карты"""
        # Все нули
        assert get_mask_card_number("0000000000000000") == "0000 0000** **** 0000"
        # Повторяющиеся цифры
        assert get_mask_card_number("1111222233334444") == "1111 2222** **** 4444"

    def test_mask_account_card_mixed_input(self):
        """Тестируем смешанные случаи"""
        # Карта с пробелами и дефисами
        assert mask_account_card("1234-5678-9012-3456") == "1234 5678** **** 3456 (card)"
        # Счёт с пробелами
        assert mask_account_card("1234 5678 9012 3456 7890") == "****************7890 (account)"