import os
import pytest
from unittest.mock import patch
import pandas as pd

from src.utils import (
    load_transactions_from_json,
    load_transactions_from_csv,
    load_transactions_from_xlsx,
)


@pytest.fixture
def mock_json_data():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-02"},
    ]


@pytest.fixture
def mock_csv_content():
    # CSV без заголовка, разделитель ";"
    return """4234093;EXECUTED;2021-07-08T07:31:21Z;23182;Ruble;RUB;Visa;Discover;Перевод
4234094;PENDING;2021-07-09T08:32:22Z;1000;Ruble;RUB;Mastercard;Visa;Перевод"""


def test_load_json_success(mock_json_data, tmp_path):
    f = tmp_path / "ops.json"
    f.write_text(__import__("json").dumps(mock_json_data), encoding="utf-8")
    result = load_transactions_from_json(str(f))
    assert len(result) == 2
    assert result[0]["id"] == 1


def test_load_json_empty_list(tmp_path):
    f = tmp_path / "empty.json"
    f.write_text("[]", encoding="utf-8")
    result = load_transactions_from_json(str(f))
    assert result == []


def test_load_csv_without_header(mock_csv_content, tmp_path):
    f = tmp_path / "ops.csv"
    f.write_text(mock_csv_content, encoding="utf-8")
    result = load_transactions_from_csv(str(f))
    assert len(result) == 2
    assert result[0]["state"] == "EXECUTED"
    assert result[1]["state"] == "PENDING"


def test_load_csv_empty(tmp_path):
    f = tmp_path / "empty.csv"
    f.write_text("", encoding="utf-8")
    result = load_transactions_from_csv(str(f))
    assert result == []


@patch("src.utils.pd.read_excel")
def test_load_xlsx_success(mock_read_excel, tmp_path):
    mock_df = pd.DataFrame([{"id": 99, "state": "EXECUTED"}])
    mock_read_excel.return_value = mock_df
    result = load_transactions_from_xlsx("dummy.xlsx")
    assert len(result) == 1
    assert result[0]["id"] == 99


@patch("src.utils.pd.read_excel")
def test_load_xlsx_import_error_returns_empty(mock_read_excel):
    mock_read_excel.side_effect = ImportError("No openpyxl")
    result = load_transactions_from_xlsx("dummy.xlsx")
    # Функция должна быть устойчивой: вернуть [], а не выбросить ошибку
    assert result == []
    mock_read_excel.assert_called_once()


def test_load_csv_no_obvious_header(tmp_path):
    f = tmp_path / "no-header-clue.csv"
    # Первая строка НЕ начинается с id/state/date — логика должна считать, что заголовка нет
    f.write_text(
        "4234093;EXECUTED;2021-07-08T07:31:21Z;23182;Ruble;RUB;Visa;Discover;Перевод\n",
        encoding="utf-8",
    )
    result = load_transactions_from_csv(str(f))
    assert len(result) == 1
    assert result[0]["state"] == "EXECUTED"


def test_load_csv_skip_invalid_row(tmp_path):
    f = tmp_path / "bad-row.csv"
    f.write_text(
        "id;state;date;amount;currency_name;currency_code;from;to;description\n"
        "4234094;;2021-07-09T08:32:22Z;1000;Ruble;RUB;Mastercard;Visa;Перевод\n"  # нет state
        "4234095;EXECUTED;2021-07-10T09:00:00Z;500;Ruble;RUB;Visa;Mastercard;Оплата\n",
        encoding="utf-8",
    )
    result = load_transactions_from_csv(str(f))
    # Должна остаться только одна валидная строка
    assert len(result) == 1
    assert result[0]["id"] == "4234095"


def test_load_csv_file_not_found(tmp_path):
    # Путь к несуществующему файлу
    fake_path = os.path.join(str(tmp_path), "no-such-file.csv")
    result = load_transactions_from_csv(fake_path)
    assert result == []
