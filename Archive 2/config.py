import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://telranedu.web.app/home")

API_URL = os.getenv(
    "API_URL", "https://contactapp-telran-backend.herokuapp.com"
)

DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", 5))
VALID_EMAIL = os.getenv("VALID_EMAIL")
VALID_PASSWORD = os.getenv("VALID_PASSWORD")