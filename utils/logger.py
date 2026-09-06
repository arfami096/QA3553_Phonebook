import logging


def get_logger(name=__name__):
  logger = logging.getLogger(name)
  if not logger.handlers:
    logger.setLevel(logging.INFO)

    # Настраиваем понятный формат: дата/время, уровень, название модуля и сообщение
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Добавляем StreamHandler для вывода в поток (stderr/stdout)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Отключаем всплытие к корневому логгеру, чтобы избежать лишних дублей
    logger.propagate = False

  return logger

#Логирование
#Настройка единого логера (logging), чтобы в консоли и отчетах фиксировались ключевые шаги (открытие страниц, клики, ввод данных).