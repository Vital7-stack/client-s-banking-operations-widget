import unittest

from src.masks import (
    get_date,
    get_mask_account,
    get_mask_card_number,
    mask_account_card,
)


class TestMasksFunctions(unittest.TestCase):
    # --- get_mask_account ---
    def test_get_mask_account_valid_full(self) -> None:
        # Стандартный случай: 20 цифр
        self.assertEqual(
            get_mask_account("12345678901234567890"),
            "****************7890",
        )
        # Специальный случай: ровно 4 цифры -> 4 звезды
        self.assertEqual(get_mask_account("1234"), "****")

    def test_get_mask_account_invalid_length(self) -> None:
        # Слишком коротко
        with self.assertRaises(ValueError):
            get_mask_account("123")
        with self.assertRaises(ValueError):
            get_mask_account("")
        with self.assertRaises(ValueError):
            get_mask_account("   ")

    def test_get_mask_account_invalid_type(self) -> None:
        with self.assertRaises(TypeError):
            get_mask_account(123)  # type: ignore
        with self.assertRaises(TypeError):
            get_mask_account([1, 2, 3])  # type: ignore
        with self.assertRaises(TypeError):
            get_mask_account(None)  # type: ignore

    def test_get_mask_account_non_digit(self) -> None:
        with self.assertRaises(ValueError):
            get_mask_account("1234ABCD")
        with self.assertRaises(ValueError):
            get_mask_account("12A-34B")  # Дефисы уже удаляются, но если после очистки не цифры - ошибка

    # --- get_mask_card_number ---
    def test_get_mask_card_number_valid(self) -> None:
        result = get_mask_card_number("1234-5678-9012-3456")
        self.assertEqual(result, "1234 56** **** 3456")

        result_with_spaces = get_mask_card_number("1234 5678 9012 3456")
        self.assertEqual(result_with_spaces, "1234 56** **** 3456")

    def test_get_mask_card_number_invalid(self) -> None:
        # Неверная длина
        with self.assertRaises(ValueError):
            get_mask_card_number("123456789012345")  # 15 цифр
        with self.assertRaises(ValueError):
            get_mask_card_number("1" * 17)  # 17 цифр

        # Нецифровые символы (после очистки остаются буквы)
        with self.assertRaises(ValueError):
            get_mask_card_number("1234abcd5678efgh")

        # Пустая строка
        with self.assertRaises(ValueError):
            get_mask_card_number("")

    # --- mask_account_card (автоматическое распознавание) ---
    def test_mask_account_card_valid_card(self) -> None:
        self.assertEqual(
            mask_account_card("1234567812345678"),
            "1234 56** **** 5678 (card)",
        )

    def test_mask_account_card_valid_account_exactly_20(self) -> None:
        res = mask_account_card("1" * 20)
        self.assertTrue(res.endswith("(account)"))
        self.assertIn("****", res)  # Проверяем, что маска применилась

    def test_mask_account_card_invalid_input_types(self) -> None:
        self.assertEqual(mask_account_card(None), "invalid input")
        self.assertEqual(mask_account_card(""), "invalid input")
        self.assertEqual(mask_account_card("   "), "invalid input")
        self.assertEqual(mask_account_card(123), "invalid input")  # type: ignore

    def test_mask_account_card_edge_lengths(self) -> None:
        # Длины, не равные 16 и не равные 20 → invalid input
        self.assertEqual(mask_account_card("1" * 15), "invalid input")
        self.assertEqual(mask_account_card("1" * 17), "invalid input")
        self.assertEqual(mask_account_card("1" * 19), "invalid input")
        self.assertEqual(mask_account_card("1" * 22), "invalid input")

    def test_mask_account_card_with_separators(self) -> None:
        s_dirty = "1234-5678-1234-5678"
        expected = "1234 56** **** 5678 (card)"
        self.assertEqual(mask_account_card(s_dirty), expected)

        s_tabs = "1234\t5678\t1234\t5678"
        self.assertEqual(mask_account_card(s_tabs), expected)

    # --- get_date ---
    def test_get_date_none_empty_whitespace(self) -> None:
        self.assertEqual(get_date(None), "")
        self.assertEqual(get_date(""), "")
        self.assertEqual(get_date("   "), "")

    def test_get_date_valid_iso(self) -> None:
        self.assertEqual(get_date("2024-06-15T14:30:00"), "15.06.2024")
        self.assertEqual(get_date("2024-06-15"), "15.06.2024")

    def test_get_date_invalid_formats(self) -> None:
        self.assertEqual(get_date("15.06.2024"), "")
        self.assertEqual(get_date("not a date"), "")
        self.assertEqual(get_date("2024/06/15"), "")
        self.assertEqual(get_date("32-01-2024"), "")
        self.assertEqual(get_date("2024-13-01"), "")
        self.assertEqual(get_date("2024-02-30"), "")

    # --- consistency checks ---
    def test_formatting_consistency_card(self) -> None:
        result = get_mask_card_number("1234567890123456")
        self.assertEqual(result.count(" "), 3)
        self.assertEqual(len(result.replace(" ", "")), 16)

    def test_formatting_consistency_account(self) -> None:
        result_account = get_mask_account("12345678901234567890")
        self.assertTrue(result_account.endswith("7890"))
        self.assertIn("*", result_account)


if __name__ == "__main__":
    unittest.main()
