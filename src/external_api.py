import logging
import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_currency(
        amount: float,
        from_currency: str,
        to_currency: str = "RUB",
) -> float:
    """
    Конвертирует сумму из одной валюты в другую.

    По умолчанию конвертирует в RUB.
    Если from_currency == to_currency, просто возвращает amount.
    """
    if not API_KEY:
        logger.error("Не задан API_KEY для конвертации валют")
        return 0.0

    if from_currency.upper() == to_currency.upper():
        return round(float(amount), 2)

    try:
        params = {
            "access_key": API_KEY,
            "base": from_currency.upper(),
            "symbols": to_currency.upper(),
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()

        rates: Dict[str, float] = data.get("rates", {})
        rate: Optional[float] = rates.get(to_currency.upper())

        if rate is None:
            logger.warning(
                "Курс не найден: %s -> %s",
                from_currency.upper(),
                to_currency.upper(),
            )
            return 0.0

        return round(float(amount) * rate, 2)

    except requests.RequestException as e:
        logger.exception("Ошибка запроса к API конвертации: %s", e)
        return 0.0
    except Exception as e:
        # Ловим всё остальное, чтобы функция не падала
        logger.exception("Неожиданная ошибка при конвертации: %s", e)
        return 0.0


def fetch_operations(
        url: str,
        token: str,
) -> list[dict[str, Any]]:
    """Получает список операций из внешнего API."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        # Нормализуем разные возможные структуры ответа
        if isinstance(data, list):
            return data

        if not isinstance(data, dict):
            logger.warning("Неожиданный формат ответа от API операций: %s", type(data))
            return []

        if "operations" in data and isinstance(data["operations"], list):
            return data["operations"]

        if "data" in data and isinstance(data["data"], list):
            return data["data"]

        logger.warning("Не удалось найти список операций в ответе API")
        return []

    except requests.RequestException as e:
        logger.exception("Ошибка запроса к API операций: %s", e)
        return []
    except ValueError as e:
        # JSON decode error
        logger.exception("Ошибка декодирования JSON в ответе API операций: %s", e)
        return []
    except Exception as e:
        logger.exception("Неожиданная ошибка при получении операций: %s", e)
        return []
