import uuid

import requests

from config import API_URL


def test_registration_success():
    unique_email = f"student_{uuid.uuid4().hex[:8]}@gmail.com"

    payload={
        "username":unique_email,
        "password": "Password!123"
    }

    requests.post(f"{API_URL}")