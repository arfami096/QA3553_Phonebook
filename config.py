import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://telranedu.web.app/home")
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", 5))

# Тестовые учетные данные подтягиваются из скрытого файла
VALID_EMAIL = os.getenv("VALID_EMAIL")
VALID_PASSWORD = os.getenv("VALID_PASSWORD")