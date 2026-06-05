
from unittest.mock import patch, Mock
from src.external_api import convert_currency

class TestConvertCurrency:
    @patch('requests.get')
    def test_usd_to_rub(self, mock_get):  # self убран, если не используется
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'rates': {'RUB': 90.5}}
        mock_get.return_value = mock_response

        x_usd = {
            "operationAmount": {
                "amount": "10",
                "currency": {"name": "USD", "code": "USD"}
            }
        }

        # Переименовали локальную переменную, чтобы не конфликтовать с возможной внешней
        converted_amount = convert_currency(x_usd)
        assert converted_amount == 905.0

    def test_rub_no_conversion(self):
        transaction = {
            "operationAmount": {
                "amount": "1000",
                "currency": {
                    "name": "RUB",
                    "code": "RUB"
                }
            }
        }
        result = convert_currency(transaction)
        assert result == 1000.0