from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.transactions_reader import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)


@patch("src.transactions_reader.Path.exists")
@patch("src.transactions_reader.pd.read_csv")
def test_read_transactions_from_csv_success(mock_read_csv: MagicMock, mock_exists: MagicMock) -> None:
    """Тест успешного чтения CSV с использованием mock."""
    mock_exists.return_value = True

    mock_df = MagicMock()
    mock_df.empty = False
    mock_df.to_dict.return_value = [
        {"id": 1, "amount": 100.0, "currency": "RUB"},
        {"id": 2, "amount": 200.5, "currency": "USD"},
    ]
    mock_read_csv.return_value = mock_df

    result = read_transactions_from_csv("transactions.csv")

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["id"] == 1
    # Проверяем, что внутрь передали Path (если функция так делает)
    mock_read_csv.assert_called_once_with(Path("transactions.csv"))


@patch("src.transactions_reader.Path.exists")
@patch("src.transactions_reader.pd.read_csv")
def test_read_transactions_from_csv_file_not_found(mock_read_csv: MagicMock, mock_exists: MagicMock) -> None:
    """Тест ошибки, если CSV-файл не найден."""
    mock_exists.return_value = False

    with pytest.raises(FileNotFoundError):
        read_transactions_from_csv("missing.csv")

    mock_read_csv.assert_not_called()


@patch("src.transactions_reader.Path.exists")
@patch("src.transactions_reader.pd.read_csv")
def test_read_transactions_from_csv_empty_file(mock_read_csv: MagicMock, mock_exists: MagicMock) -> None:
    """Тест обработки пустого CSV-файла."""
    mock_exists.return_value = True

    mock_df = MagicMock()
    mock_df.empty = True
    mock_read_csv.return_value = mock_df

    # Внимание: этот тест пройдёт только если в функции есть raise ValueError при empty
    with pytest.raises(ValueError):
        read_transactions_from_csv("empty.csv")


# --- ВОТ ЭТОТ БЛОК МЫ ВСТАВЛЯЕМ ВМЕСТО СТАРОГО test_read_transactions_from_excel_success ---
@patch("src.transactions_reader.Path.is_file")
@patch("src.transactions_reader.Path.exists")
@patch("src.transactions_reader.pd.read_excel")
def test_read_transactions_from_excel_success(
    mock_read_excel: MagicMock, mock_exists: MagicMock, mock_is_file: MagicMock
) -> None:
    """Тест успешного чтения Excel с использованием mock."""
    mock_exists.return_value = True
    mock_is_file.return_value = True  # Подменяем и is_file, чтобы не было ValueError

    mock_df = MagicMock()
    mock_df.empty = False
    mock_df.to_dict.return_value = [
        {"id": 3, "amount": 300.0, "currency": "EUR"},
        {"id": 4, "amount": 400.2, "currency": "CNY"},
    ]
    mock_read_excel.return_value = mock_df

    result = read_transactions_from_excel("transactions_excel.xlsx")

    assert result == [
        {"id": 3, "amount": 300.0, "currency": "EUR"},
        {"id": 4, "amount": 400.2, "currency": "CNY"},
    ]
    mock_read_excel.assert_called_once()


# ---------------------------------------------------------------------------------------------


@patch("src.transactions_reader.Path.exists")
@patch("src.transactions_reader.pd.read_excel")
def test_read_transactions_from_excel_file_not_found(
    mock_read_excel: MagicMock, mock_exists: MagicMock
) -> None:
    """Тест ошибки, если Excel-файл не найден."""
    mock_exists.return_value = False

    with pytest.raises(FileNotFoundError):
        read_transactions_from_excel("missing.xlsx")

    mock_read_excel.assert_not_called()


@patch("src.transactions_reader.Path.exists")
@patch("src.transactions_reader.pd.read_excel")
def test_read_transactions_from_excel_empty_sheet(
    mock_read_excel: MagicMock, mock_exists: MagicMock
) -> None:
    """Тест обработки пустого листа в Excel."""
    mock_exists.return_value = True

    mock_df = MagicMock()
    mock_df.empty = True
    mock_read_excel.return_value = mock_df

    with pytest.raises(ValueError):
        read_transactions_from_excel("empty.xlsx")
