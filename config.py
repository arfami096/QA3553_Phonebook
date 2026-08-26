import os

BASE_URL = os.getenv("BASE_URL", "https://telranedu.web.app/home")
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", 5))

# Тестовые учетные данные
VALID_EMAIL = os.getenv("VALID_EMAIL", "arfami096@gmail.com")
VALID_PASSWORD = os.getenv("VALID_PASSWORD", "Jamalungma08!")