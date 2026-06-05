import unittest
import json
import logging
import os
import tempfile  # Правильный импорт

from src.utils import (
    calculate_sum,
    read_json_file,
    validate_data,
)
from src.masks import (
    get_mask_card_number,
    get_mask_account,
)

class TestUtilsFunctions(unittest.TestCase):
    """Тесты для utils.py, которые проверяют результат работы функций."""

    def setUp(self):
        # Создаём временную директорию для логов
        self.temp_dir = tempfile.TemporaryDirectory()
        # Сохраняем оригинальный логгер для восстановления после теста
        self.original_logger = logging.getLogger('utils')

    def tearDown(self):
        # Закрываем обработчики логгера
        for handler in self.original_logger.handlers[:]:
            handler.close()
            self.original_logger.removeHandler(handler)
        # Чистим за собой после каждого теста
        self.temp_dir.cleanup()

    # --- ТЕСТЫ ДЛЯ ФУНКЦИЙ С ЛОГИРОВАНИЕМ ---

    def test_calculate_sum_success(self):
        """Тест успешного случая calculate_sum."""
        result = calculate_sum(2, 3)
        self.assertEqual(result, 5)

    def test_calculate_sum_none_error(self):
        """Тест ошибки при передаче None."""
        with self.assertRaises(ValueError):
            calculate_sum(None, 5)
        with self.assertRaises(ValueError):
            calculate_sum(5, None)

    def test_calculate_sum_type_error(self):
        """Тест ошибки при некорректных типах."""
        with self.assertRaises(TypeError):
            calculate_sum("abc", 5)
        with self.assertRaises(TypeError):
            calculate_sum(5, "abc")
        with self.assertRaises(TypeError):
            calculate_sum("abc", "def")
    def test_read_json_file_valid(self):
        """Тест чтения корректного JSON-файла."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([{'id': 1}], f)
            temp_file_path = f.name

        try:
            result = read_json_file(temp_file_path)
            self.assertEqual(result, [{'id': 1}])
        finally:
            os.remove(temp_file_path)

    def test_validate_data_valid(self):
        """Тест успешного случая validate_data."""
        result = validate_data("test string")
        self.assertTrue(result)

    def test_validate_data_none(self):
        """Тест ошибочного случая: данные None."""
        with self.assertRaises(ValueError) as context:
            validate_data(None)
        self.assertIn("Данные не могут быть None", str(context.exception))

    def test_validate_data_not_string(self):
        """Тест ошибочного случая: данные не строка."""
        with self.assertRaises(ValueError) as context:
            validate_data(123)
        self.assertIn("Данные должны быть строкой", str(context.exception))

    def test_validate_data_empty_string(self):
        """Тест ошибочного случая: пустая строка."""
        with self.assertRaises(ValueError) as context:
            validate_data("")
        self.assertIn("Данные не могут быть пустой строкой", str(context.exception))

    def test_read_json_file_invalid_json(self):
        """Тест чтения некорректного JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"key": invalid}')
            temp_file_path = f.name

        try:
            result = read_json_file(temp_file_path)
            self.assertEqual(result, [])
        finally:
            os.remove(temp_file_path)

    def test_read_json_file_not_found(self):
        """Тест при отсутствии файла."""
        result = read_json_file('/path/to/nonexistent/file.json')
        self.assertEqual(result, [])


class TestMasksFunctions(unittest.TestCase):
    """Тесты для masks.py, которые проверяют результат работы функций."""

    def setUp(self):
        # Создаём временную директорию для логов
        self.temp_dir = tempfile.TemporaryDirectory()
        # Сохраняем оригинальный логгер для восстановления после теста
        self.original_logger = logging.getLogger('masks')

    def tearDown(self):
        # Закрываем обработчики логгера
        for handler in self.original_logger.handlers[:]:
            handler.close()
            self.original_logger.removeHandler(handler)
        # Чистим за собой после каждого теста
        self.temp_dir.cleanup()

    def get_test_mask_card_number_success(self):
        """Тест успешного маскирования номера карты."""
        result = get_mask_card_number("1234 5678 9012 3456")
        self.assertEqual(result, "1234 56** **** 3456")

    def test_get_mask_card_number_invalid(self):
        """Тест ошибочного маскирования номера карты (некорректный формат)."""
        with self.assertRaises(ValueError):
            get_mask_card_number("123")

    def test_get_mask_account_success(self):
        """Тест успешного маскирования номера счёта."""
        result = get_mask_account("12345678901234567890")
        # Исправлен формат: все цифры, кроме последних 4, заменены на *
        self.assertEqual(result, "****************7890")

    def test_get_mask_account_invalid(self):
        """Тест ошибочного маскирования номера счёта (некорректный формат)."""
        with self.assertRaises(ValueError):
            get_mask_account("abc")