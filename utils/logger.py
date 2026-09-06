import logging


def get_logger(name=__name__):
  logger = logging.getLogger(name)
  # Если хэндлеров еще нет, просто задаем уровень.
  # Никаких StreamHandler создавать НЕ нужно!
  if not logger.handlers:
    logger.setLevel(logging.INFO)
  return logger

#Логирование
#Настройка единого логера (logging), чтобы в консоли и отчетах фиксировались ключевые шаги (открытие страниц, клики, ввод данных).