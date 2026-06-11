import json
from unittest.mock import patch
from src.main import main


@patch(
    "builtins.input",
    side_effect=[
        "1", "test.json", "EXECUTED",
        "нет", "нет", "нет", "нет"
    ],
)
@patch("src.main.load_transactions_from_json", return_value=[])
def test_main_basic_flow(mock_load, mock_input):  # noqa: F841
    main()


@patch(
    "builtins.input",
    side_effect=[
        "2", "test.csv", "EXECUTED",
        "да", "по возрастанию",
        "нет", "нет", "нет"
    ],
)
@patch("src.main.load_transactions_from_csv", return_value=[
    {"date": "2024-01-01", "description": "test"}
])
def test_main_csv_with_sort(mock_load, mock_input):  # noqa: F841
    main()


@patch(
    "builtins.input",
    side_effect=[
        "3", "test.xlsx", "EXECUTED",
        "да", "по убыванию",
        "да", "pay",
        "неверный ответ",
        "нет"
    ],
)
@patch("src.main.load_transactions_from_xlsx", return_value=[
    {"date": "2024-01-02", "description": "pay", "currency": "RUB", "from_account": "1234", "to_account": "5678"},
    {"date": "2024-01-01", "description": "transfer", "currency": "USD", "from_account": "9999", "to_account": "8888"},
])
def test_main_xlsx_full_flow(mock_load, mock_input):  # noqa: F841
    main()


@patch(
    "builtins.input",
    side_effect=[
        "1", "test.json",
        "INVALID_STATE",
        "EXECUTED",
        "нет", "нет", "нет", "нет"
    ],
)
@patch("src.main.load_transactions_from_json", return_value=[{"state": "EXECUTED"}])
def test_main_ask_state_retry(mock_load, mock_input):  # noqa: F841
    main()


@patch(
    "builtins.input",
    side_effect=["1", "missing.json"]
)
@patch("src.main.load_transactions_from_json", side_effect=FileNotFoundError("no file"))
def test_main_file_not_found(mock_load, mock_input):  # noqa: F841
    main()


@patch(
    "builtins.input",
    side_effect=["1", "bad.json"]
)
@patch("src.main.load_transactions_from_json", side_effect=json.JSONDecodeError("bad json", "", 0))
def test_main_invalid_json(mock_load, mock_input):  # noqa: F841
    main()

@patch(
    "builtins.input",
    side_effect=[
        "1", "test.json", "EXECUTED",
        "да", "по убыванию",          # сортировка по убыванию
        "нет",                        # только RUB — нет
        "да",                         # поиск по описанию — да
        "перевод",                    # слово для поиска
        "нет"                         # дальше ничего не нужно
    ],
)
@patch("src.main.load_transactions_from_json", return_value=[
    {"date": "2024-01-03", "description": "Перевод организации", "currency": "RUB"},
    {"date": "2024-01-02", "description": "Снятие наличных", "currency": "USD"},
])
def test_main_full_filter_flow(mock_load, mock_input):  # noqa: F841
    main()


@patch(
    "builtins.input",
    side_effect=[
        "2", "test.csv", "CANCELED",
        "нет", "нет", "нет"
    ],
)
@patch("src.main.load_transactions_from_csv", return_value=[])
def test_main_csv_empty_result(mock_load, mock_input):  # noqa: F841
    # Проверяем, что программа корректно обрабатывает пустой список
    main()


@patch(
    "builtins.input",
    side_effect=[
        "3", "test.xlsx", "PENDING",
        "да", "по возрастанию",
        "да",                         # только RUB
        "нет"                         # без поиска по описанию
    ],
)
@patch("src.main.load_transactions_from_xlsx", return_value=[
    {"date": "2024-01-01", "description": "Оплата услуг", "currency": "RUB", "from_account": "1111", "to_account": "2222"},
    {"date": "2024-01-02", "description": "Перевод", "currency": "EUR", "from_account": "3333", "to_account": "4444"},
])
def test_main_xlsx_rub_only_flow(mock_load, mock_input):  # noqa: F841
    main()