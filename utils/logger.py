import logging
import os


def get_logger(name=__name__, log_file="test_execution.log"):
  logger = logging.getLogger(name)

  # Проверяем, чтобы у логгера не плодились дублирующие хэндлеры при импортах
  if not logger.handlers:
    logger.setLevel(logging.INFO)

    # Единый формат: время, уровень, имя модуля и само сообщение
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 1. Вывод в консоль (StreamHandler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # 2. Запись в файл (FileHandler)
    os.makedirs("logs", exist_ok=True)
    file_path = os.path.join("logs", log_file)
    file_handler = logging.FileHandler(file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Отключаем передачу логов корневому логгеру, чтобы не было дублей
    logger.propagate = False

  return logger

#Логирование
#Настройка единого логера (logging), чтобы в консоли и отчетах фиксировались ключевые шаги (открытие страниц, клики, ввод данных).