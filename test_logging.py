import os
import logging

# Создаём папку logs, если её нет
os.makedirs('logs', exist_ok=True)

# Настраиваем логгер для модуля utils
utils_logger = logging.getLogger('utils')
utils_logger.setLevel(logging.DEBUG)

# Очищаем существующие handler'ы
utils_logger.handlers.clear()

# Форматирование логов
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# FileHandler с перезаписью при каждом запуске
utils_handler = logging.FileHandler('logs/utils.log', mode='w', encoding='utf-8')
utils_handler.setFormatter(formatter)
utils_logger.addHandler(utils_handler)

# Аналогично для модуля masks
masks_logger = logging.getLogger('masks')
masks_logger.setLevel(logging.DEBUG)
masks_logger.handlers.clear()

masks_handler = logging.FileHandler('logs/masks.log', mode='w', encoding='utf-8')
masks_handler.setFormatter(formatter)
masks_logger.addHandler(masks_handler)

# Пишем логи в требуемом формате
utils_logger.info("Функция some_utility_function успешно выполнена")
masks_logger.error("Ошибка при применении маски: Some error")

print("✅ Проверка завершена!")
print("📁 Проверьте папку 'logs' — в ней должны появиться файлы:")
print("   - utils.log")
print("   - masks.log")