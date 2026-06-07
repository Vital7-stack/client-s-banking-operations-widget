from typing import Optional

import pytest

from src.widget import get_date, mask_account_card


class TestWidget:
    @pytest.mark.parametrize(
        "input_data,expected_type",
        [
            ("1234567890123456", "card"),
            ("1234 5678 9012 3456", "card"),
            ("12345678901234567890", "account"),
            ("1234 5678 9012 3456 7890", "account"),
        ],
    )
    def test_mask_account_card_type_recognition(self, input_data: str, expected_type: str) -> None:
        """Проверка распознавания типа данных (карта/счёт)."""
        result: str = mask_account_card(input_data)
        assert expected_type in result.lower()

    @pytest.mark.parametrize(
        "date_input,expected_format",
        [
            ("2023-01-01", "01.01.2023"),
            ("2023-12-25T10:30:00", "25.12.2023"),
            ("", ""),
            (None, ""),
        ],
    )
    def test_get_date_formatting(self, date_input: Optional[str], expected_format: str) -> None:
        """Тестирование преобразования даты в различные форматы."""
        result: str = get_date(date_input)
        assert result == expected_format
