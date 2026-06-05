import unittest
from src.masks import (
    get_mask_account,
    get_mask_card_number,
    mask_account_card,
)

class TestMasksFunctions(unittest.TestCase):
    def test_get_mask_account_valid(self):
        """Тест корректной работы маскирования счёта."""
        self.assertEqual(get_mask_account("12345678901234567890"), "****************7890")
        self.assertEqual(get_mask_account("1234"), "****")

    def test_get_mask_account_invalid_length(self):
        """Тест обработки слишком короткого номера счёта."""
        with self.assertRaises(ValueError):
            get_mask_account("123")
        with self.assertRaises(ValueError):
            get_mask_account("")

    def test_get_mask_account_invalid_type(self):
        """Тест обработки некорректных типов данных для счёта."""
        with self.assertRaises(TypeError):
            get_mask_account(123)  # type: ignore
        with self.assertRaises(TypeError):
            get_mask_account([1, 2, 3])  # type: ignore
        with self.assertRaises(TypeError):
            get_mask_account(None)  # type: ignore

    def test_get_mask_card_number_valid(self):
        """Тест корректной работы маскирования карты."""
        result = get_mask_card_number("1234-5678-9012-3456")
        self.assertEqual(result, "1234 56** **** 3456")
        result_with_spaces = get_mask_card_number("1234 5678 9012 3456")
        self.assertEqual(result_with_spaces, "1234 56** **** 3456")

    def test_get_mask_card_number_invalid(self):
        """Тест обработки некорректных данных для карты."""
        with self.assertRaises(ValueError):
            get_mask_card_number("123456789012345")  # 15 цифр
        with self.assertRaises(ValueError):
            get_mask_card_number("1234abcd5678efgh")  # буквы
        with self.assertRaises(ValueError):
            get_mask_card_number("")  # пустая строка


    def test_mask_account_card_valid(self):
        """Тест корректной работы автоматического распознавания."""
        self.assertEqual(
            mask_account_card("1234567890123456"),
            "1234 56** **** 3456 (card)"
        )
        self.assertEqual(
            mask_account_card("12345678901234567890"),
            "****************7890 (account)"
        )

    def test_mask_account_card_invalid(self):
        """Тест обработки некорректных входных данных."""
        self.assertEqual(mask_account_card(None), "invalid input")
        self.assertEqual(mask_account_card(""), "invalid input")
        self.assertEqual(mask_account_card("abc"), "invalid input")
        self.assertEqual(mask_account_card("123"), "invalid input")  # слишком короткий номер


    def test_mask_account_card_with_dashes(self):
        """Тест обработки номеров с дефисами."""
        self.assertEqual(
            mask_account_card("1234-5678-9012-3456"),
            "1234 56** **** 3456 (card)"
        )
        self.assertEqual(
            mask_account_card("1234-5678-9012-3456-7890"),
            "****************7890 (account)"
        )

    def test_edge_cases_account(self):
        """Тест граничных случаев для счёта."""
        self.assertEqual(get_mask_account("1234"), "****")
        long_account = "1" * 25
        expected_long = "*" * 21 + "1111"
        self.assertEqual(get_mask_account(long_account), expected_long)

    def test_edge_cases_card(self):
        """Тест граничных случаев для карты."""
        self.assertEqual(
            get_mask_card_number("1111222233334444"),
            "1111 22** **** 4444"
        )

    def test_formatting_consistency_card(self):
        """Тест согласованности форматирования маски карты."""
        result = get_mask_card_number("1234567890123456")
        self.assertEqual(result.count(" "), 3)
        self.assertEqual(len(result.replace(" ", "")), 16)

    def test_formatting_consistency_account(self):
        """Тест согласованности форматирования маски счёта."""
        result_account = get_mask_account("12345678901234567890")
        self.assertEqual(len(result_account), 20)

if __name__ == '__main__':
    unittest.main()