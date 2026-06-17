from typing import Optional

import pytest
from src.masks import get_mask_account, get_mask_card_number, mask_account_card


class TestMasks:
    @pytest.mark.parametrize(
        "account_input,expected_output",
        [
            ("12345678901234567890", "****************7890"),
            ("1234", "****"),
            ("", ""),
            (None, ""),
            ("   ", ""),
        ],
    )
    def test_get_mask_account(
        self, account_input: Optional[str], expected_output: str
    ) -> None:
        assert get_mask_account(account_input) == expected_output

    @pytest.mark.parametrize(
        "card_input,expected_output",
        [
            ("1234567890123456", "1234 5678** **** 3456"),
            ("1234 5678 9012 3456", "1234 5678** **** 3456"),
            ("1234-5678-9012-3456", "1234 5678** **** 3456"),
            ("12345", ""),
            ("abcd123456789012", ""),
        ],
    )
    def test_get_mask_card_number(self, card_input: str, expected_output: str) -> None:
        assert get_mask_card_number(card_input) == expected_output

    @pytest.mark.parametrize(
        "input_data,expected_contains",
        [
            ("1234567890123456", "(card)"),
            ("1234 5678 9012 3456", "(card)"),
            ("12345678901234567890", "(account)"),
            ("1234 5678 9012 3456 7890", "(account)"),
            ("12345", "invalid input"),
            ("abc123456789012", "invalid input"),
        ],
    )
    def test_mask_account_card_type_recognition(
        self, input_data: str, expected_contains: str
    ) -> None:
        result = mask_account_card(input_data)
        assert expected_contains in result
