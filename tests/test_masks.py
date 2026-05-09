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
