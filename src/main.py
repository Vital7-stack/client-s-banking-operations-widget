import logging
from pathlib import Path

from .external_api import convert_currency
from .utils import read_json_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    config_path = Path("config.json")
    logger.info("Читаем конфиг: %s", config_path)

    config = read_json_file(str(config_path))
    if not config:
        logger.error("Конфиг не загружен")
        return

    amount_rub = 1000
    # Позиционные аргументы: mypy их точно примет
    amount_usd = convert_currency(amount_rub, "RUB", "USD")

    logger.info("Конвертация: %s RUB = %s USD", amount_rub, amount_usd)


if __name__ == "__main__":
    main()
