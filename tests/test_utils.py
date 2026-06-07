import json
import logging
import os
import tempfile
import unittest


from src.utils import calculate_sum, convert_currency, read_json_file, validate_data


class TestUtilsFunctions(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_logger = logging.getLogger("utils")

    def tearDown(self) -> None:
        # Чистим хендлеры, чтобы не дублировались между тестами
        for handler in self.original_logger.handlers[:]:
            handler.close()
            self.original_logger.removeHandler(handler)
        self.temp_dir.cleanup()

    # --- calculate_sum ---
    def test_calculate_sum_success(self) -> None:
        self.assertEqual(calculate_sum(2, 3), 5.0)

    def test_calculate_sum_none_error(self) -> None:
        # Проверяем, что при None кидается ValueError
        with self.assertRaises(ValueError):
            calculate_sum(None, 5)  # type: ignore
        with self.assertRaises(ValueError):
            calculate_sum(5, None)  # type: ignore
        with self.assertRaises(ValueError):
            calculate_sum(None, None)  # type: ignore

    def test_calculate_sum_type_error(self) -> None:
        # Проверяем, что при неверных типах кидается TypeError
        with self.assertRaises(TypeError):
            calculate_sum("abc", 5)  # type: ignore
        with self.assertRaises(TypeError):
            calculate_sum(5, "abc")  # type: ignore
        with self.assertRaises(TypeError):
            calculate_sum("abc", "def")  # type: ignore
        with self.assertRaises(TypeError):
            calculate_sum([], 1)  # type: ignore

    # --- read_json_file ---
    def test_read_json_file_valid(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump([{"id": 1}], f)
            temp_file_path = f.name

        try:
            result = read_json_file(temp_file_path)
            self.assertEqual(result, [{"id": 1}])
        finally:
            os.remove(temp_file_path)

    def test_read_json_file_invalid_json(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write('{"key": invalid}')
            temp_file_path = f.name

        try:
            result = read_json_file(temp_file_path)
            # Функция возвращает [] при ошибке
            self.assertEqual(result, [])
        finally:
            os.remove(temp_file_path)

    def test_read_json_file_not_found(self) -> None:
        result = read_json_file("/path/to/nonexistent/file.json")
        self.assertEqual(result, [])

    # --- validate_data ---
    def test_validate_data_valid(self) -> None:
        self.assertTrue(validate_data("test string"))

    def test_validate_data_none(self) -> None:
        with self.assertRaises(ValueError) as context:
            validate_data(None)  # type: ignore
        self.assertIn("Данные не могут быть None", str(context.exception))

    def test_validate_data_not_string(self) -> None:
        with self.assertRaises(ValueError) as context:
            validate_data(123)  # type: ignore
        self.assertIn("Данные должны быть строкой", str(context.exception))

    def test_validate_data_empty_string(self) -> None:
        with self.assertRaises(ValueError) as context:
            validate_data("")
        self.assertIn("Данные не могут быть пустой строкой", str(context.exception))

    def test_validate_data_whitespace_only(self) -> None:
        with self.assertRaises(ValueError) as context:
            validate_data("   ")
        self.assertIn("Данные не могут быть пустой строкой", str(context.exception))

    def test_calculate_sum_float_success(self) -> None:
        # Проверяем, что float тоже работает и возвращается float
        self.assertEqual(calculate_sum(2.5, 3.5), 6.0)
        self.assertIsInstance(calculate_sum(1.0, 2.0), float)

    def test_convert_currency_float_inputs(self) -> None:
        # Покрываем ветку с float в convert_currency
        self.assertAlmostEqual(convert_currency(100.5, 1.2), 120.6)

    def test_convert_currency_type_error(self) -> None:
        # Покрываем TypeError в convert_currency (когда тип не число)
        with self.assertRaises(TypeError):
            convert_currency("100", 1.2)  # type: ignore
        with self.assertRaises(TypeError):
            convert_currency(100, "1.2")  # type: ignore
