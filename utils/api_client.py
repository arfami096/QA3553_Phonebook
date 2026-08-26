import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_user_via_api(self, email, password):
        return requests.post(f"{self.base_url}/api/login", json={"email": email, "password": password})

#Управление API / HTTP-клиент
#Для подготовки тестовых данных (создание пользователя или контактов напрямую через REST API перед UI-тестом) или очистки базы после тестов.