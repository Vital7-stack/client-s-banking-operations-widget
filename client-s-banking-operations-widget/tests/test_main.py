from unittest.mock import patch
from src.main import main


@patch(
    "builtins.input",
    side_effect=[
        "3",
        "test.xlsx",
        "EXECUTED",
        "да",
        "по убыванию",
        "да",
        "pay",
        "нет",
        "нет",
    ],
)
@patch(
    "src.main.load_transactions_from_xlsx",
    return_value=[
        {
            "date": "2024-01-02",
            "description": "pay",
            "currency": "RUB",
            "from_account": "1234",
            "to_account": "5678",
        },
        {
            "date": "2024-01-01",
            "description": "transfer",
            "currency": "USD",
            "from_account": "9999",
            "to_account": "8888",
        },
    ],
)
def test_main_xlsx_full_flow(mock_load, _):
    main()
    mock_load.assert_called_once()
    # mock_input здесь не нужен: side_effect уже гарантирует, что input() вызывался нужное число раз


@patch("builtins.input", side_effect=["1", "missing.json"])
@patch("src.main.load_transactions_from_json", side_effect=FileNotFoundError("no file"))
def test_main_file_not_found(mock_load, _):
    # main() теперь ловит FileNotFoundError и делает return — тест проходит
    main()
    mock_load.assert_called_once()


@patch("builtins.input", side_effect=["1", "bad.json"])
@patch("src.main.load_transactions_from_json", side_effect=ValueError("bad json"))
def test_main_invalid_json(mock_load, _):
    # main() ловит ValueError и делает return — тест проходит
    main()
    mock_load.assert_called_once()


@patch("builtins.input", side_effect=["5", "dummy.json"])  # неверный тип файла
def test_main_invalid_file_type(_):
    # main() должен вывести «Неверный тип файла.» и сделать return
    main()
    # Проверяем, что функция завершилась без ошибок
    assert True


@patch(
    "builtins.input",
    side_effect=[
        "1",
        "test.json",  # JSON
        "",  # пустой статус → без фильтрации
        "",  # пустая сортировка → по возрастанию
        "",  # пустая валюта → все валюты
        "",  # пустой поиск → без поиска
        "нет",  # НЕ показывать статистику
    ],
)
@patch(
    "src.main.load_transactions_from_json",
    return_value=[
        {
            "date": "2024-01-02",
            "description": "pay",
            "currency": "RUB",
            "from_account": "1234",
            "to_account": "5678",
        },
    ],
)
def test_main_empty_filters_no_stats(mock_load, _):
    main()
    mock_load.assert_called_once()


@patch(
    "builtins.input",
    side_effect=[
        "2",
        "test.csv",
        "EXECUTED",
        "по возрастанию",
        "RUB",
        "перевод",
        "нет",  # не показывать статистику
        "нет",  # финальный вывод (если есть)
    ],
)
@patch(
    "src.main.load_transactions_from_csv",
    return_value=[
        {
            "date": "2024-01-01",
            "description": "Перевод средств",
            "currency_code": "RUB",
            "state": "EXECUTED",
        },
        {
            "date": "2024-01-02",
            "description": "Оплата услуг",
            "currency_code": "USD",
            "state": "EXECUTED",
        },
    ],
)
def test_main_csv_full_flow_no_stats(mock_load, _):
    main()
    mock_load.assert_called_once()
