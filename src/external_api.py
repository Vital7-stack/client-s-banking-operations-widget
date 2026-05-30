import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем переменные из .env
API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
BASE_URL = 'https://api.apilayer.com/exchangerates_data/latest'

def convert_currency(transaction):
    """Конвертирует сумму транзакции из USD/EUR в рубли."""
    amount = transaction.get('amount', 0.0)
    currency = transaction.get('currency', 'RUB')

    if currency == 'RUB':  # Если уже рубли
        return float(amount)

    if currency not in ['USD', 'EUR']:  # Если валюта не поддерживается
        raise ValueError(f"Неподдерживаемая валюта: {currency}")

    try:
        params = {
            'access_key': API_KEY,
            'base': currency,
            'symbols': 'RUB'
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        rate = data['rates']['RUB']
        return round(float(amount) * rate, 2)  # Конвертируем и округляем до 2 знаков

    except Exception as e:
        print(f"Ошибка при конвертации: {e}")
        return 0.0