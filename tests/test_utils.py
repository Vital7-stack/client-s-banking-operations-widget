import json
from unittest.mock import mock_open, patch
from src.utils import read_json_file

class TestReadJsonFile:
    def test_file_not_found(self):
        """Тест: файл не существует — функция возвращает пустой список."""
        result = read_json_file('non_existent.json')
        assert result == []

    @patch('os.path.exists')
    def test_valid_json(self, mock_exists):
        """Тест: корректный JSON-файл со списком — функция возвращает данные."""
        mock_exists.return_value = True  # Гарантируем, что файл «существует»
        test_data = [{'id': 1, 'amount': 100}]
        with patch('builtins.open', mock_open(read_data=json.dumps(test_data))):
            result = read_json_file('dummy.json')
            assert result == test_data

    @patch('os.path.exists')
    def test_invalid_json(self, mock_exists):
        """Тест: некорректный JSON — функция возвращает пустой список."""
        mock_exists.return_value = True
        with patch('builtins.open', mock_open(read_data='{invalid json}')):
            result = read_json_file('dummy.json')
            assert result == []

    @patch('os.path.exists')
    def test_non_list_json(self, mock_exists):
        """Тест: JSON содержит объект, а не список — функция возвращает пустой список."""
        mock_exists.return_value = True
        test_data = {'id': 1, 'amount': 100}
        with patch('builtins.open', mock_open(read_data=json.dumps(test_data))):
            result = read_json_file('dummy.json')
            assert result == []

    @patch('os.path.exists')
    def test_empty_json_object(self, mock_exists):
        """Тест: пустой JSON-объект {} — функция возвращает пустой список."""
        mock_exists.return_value = True
        with patch('builtins.open', mock_open(read_data='{}')):
            result = read_json_file('dummy.json')
            assert result == []

    @patch('os.path.exists')
    def test_empty_json_array(self, mock_exists):
        """Тест: пустой JSON-массив [] — функция возвращает пустой список."""
        mock_exists.return_value = True
        with patch('builtins.open', mock_open(read_data='[]')):
            result = read_json_file('dummy.json')
            assert result == []