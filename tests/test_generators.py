import pytest
from generators.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)

@pytest.fixture
def sample_transactions() -> list[dict]:
    """Фикстура с тестовыми данными транзакций."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
            "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
            "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        }
    ]

class TestFilterByCurrency:
    def test_usd_transactions(self, sample_transactions: list[dict]) -> None:
        usd_generator = filter_by_currency(sample_transactions, "USD")
        usd_list = list(usd_generator)
        assert len(usd_list) == 2
        assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in usd_list)

    def test_rub_transactions(self, sample_transactions: list[dict]) -> None:
        rub_generator = filter_by_currency(sample_transactions, "RUB")
        rub_list = list(rub_generator)
        assert len(rub_list) == 1
        assert rub_list[0]["operationAmount"]["currency"]["code"] == "RUB"

class TestTransactionDescriptions:
    def test_descriptions_generation(self, sample_transactions: list[dict]) -> None:
        descriptions_generator = transaction_descriptions(sample_transactions)
        descriptions_list = list(descriptions_generator)
        expected = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет"
        ]
        assert descriptions_list == expected


class TestCardNumberGenerator:
    @pytest.mark.parametrize(
        "start, stop, expected",
        [
            (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
            (9999, 10001, ["0000 0000 0000 9999", "0000 0000 0001 0000"]),
        ],
    )
    def test_card_number_format(self, start: int, stop: int, expected: list[str]) -> None:
        generator = card_number_generator(start, stop)
        result = list(generator)
        assert result == expected

    def test_single_card(self) -> None:
        """Тест генерации одного номера карты."""
        generator = card_number_generator(5, 6)
        result = list(generator)
        assert result == ["0000 0000 0000 0005"]

    def test_zero_padding(self) -> None:
        """Тест заполнения нулями до 16 цифр."""
        generator = card_number_generator(1, 2)
        result = list(generator)
        assert result == ["0000 0000 0000 0001"]

    def test_large_range(self) -> None:
        """Тест генерации большого диапазона номеров с переходом через разряд."""
        generator = card_number_generator(99999999, 100000002)
        result = list(generator)
        assert len(result) == 3
        assert result[0] == "0000 0000 9999 9999"  # 99 999 999
        assert result[1] == "0000 0001 0000 0000"  # 100 000 000
        assert result[2] == "0000 0001 0000 0001"  # 100 000 001