# app_logger.py
import logging
from logging.handlers import RotatingFileHandler

# Создание логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)  # Уровень логирования настроен на ERROR

# Настройка обработчика для записи логов в файл
file_handler = RotatingFileHandler(
    "../app.log",        # Имя файла
    maxBytes=5*1024*1024,  # Максимальный размер файла (5 MB)
    backupCount=3     # Количество резервных копий логов
)
file_handler.setLevel(logging.ERROR)

# Настройка форматтера
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавление обработчика к логгеру
logger.addHandler(file_handler)
