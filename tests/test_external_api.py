
from unittest.mock import patch, Mock
from src.external_api import convert_currency

class TestConvertCurrency:
    @patch('requests.get')
    def test_usd_to_rub(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'rates': {'RUB': 90.5}}
        mock_get.return_value = mock_response

        transaction = {'amount': 10, 'currency': 'USD'}
        result = convert_currency(transaction)
        assert result == 905.0  # 10 * 90.5

    def test_rub_no_conversion(self):
        transaction = {'amount': 1000, 'currency': 'RUB'}
        result = convert_currency(transaction)
        assert result == 1000.0