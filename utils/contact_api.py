import requests

from config import API_URL, DEFAULT_TIMEOUT
from models.contact import Contact
from models.user import User

REGISTRATION_URL = "/v1/user/registration/usernamepassword"
LOGIN_URL = "/v1/user/login/usernamepassword"
CONTACTS_URL = "/v1/contacts"


class ContactApi:
    """Тонкая обёртка над requests.

    Каждый метод возвращает сырой Response: проверки (assert) делают тесты, а не клиент.
    Методы *_raw принимают готовый словарь, их удобно использовать для негативных тестов,
    где нужно отправить «сломанное» тело, которое модель собрать не даст.
    """

    def __init__(self, base_url: str = API_URL):
        self.base_url = (base_url or "").rstrip("/")
        # Быстрая проверка конфигурации: в API_URL должен быть только хост, без пути страницы
        assert self.base_url.startswith("http"), f"API_URL не задан или некорректен: {base_url!r}"
        assert "swagger" not in self.base_url and "index.html" not in self.base_url, (
            f"В API_URL лежит адрес страницы Swagger, а нужен только хост: {self.base_url}"
        )

    # ---------- служебное ----------
    @staticmethod
    def _auth_headers(token: str | None) -> dict:
        return {"Authorization": f"Bearer {token}"} if token else {}

    def _request(self, method: str, path: str, token: str | None = None, **kwargs):
        return requests.request(
            method,
            f"{self.base_url}{path}",
            headers=self._auth_headers(token),
            timeout=DEFAULT_TIMEOUT,
            **kwargs,
        )

    # ---------- пользователи ----------
    def register_raw(self, payload: dict):
        return self._request("POST", REGISTRATION_URL, json=payload)

    def register(self, user: User):
        # В API поле называется username, а в нашей модели это email
        return self.register_raw({"username": user.email, "password": user.password})

    def login_raw(self, payload: dict):
        return self._request("POST", LOGIN_URL, json=payload)

    def login(self, user: User):
        return self.login_raw({"username": user.email, "password": user.password})

    # ---------- контакты ----------
    def get_contacts(self, token: str | None = None):
        return self._request("GET", CONTACTS_URL, token)

    def add_contact_raw(self, payload: dict, token: str | None = None):
        return self._request("POST", CONTACTS_URL, token, json=payload)

    def add_contact(self, contact: Contact, token: str | None = None):
        return self.add_contact_raw(contact.to_payload(), token)

    def update_contact_raw(self, payload: dict, token: str | None = None):
        # PUT /v1/contacts: id передаётся в ТЕЛЕ запроса, а не в пути
        return self._request("PUT", CONTACTS_URL, token, json=payload)

    def update_contact(self, contact: Contact, token: str | None = None):
        return self.update_contact_raw(contact.to_payload(with_id=True), token)

    def delete_contact(self, contact_id: str, token: str | None = None):
        return self._request("DELETE", f"{CONTACTS_URL}/{contact_id}", token)

    def clear_contacts(self, token: str | None = None):
        """DELETE /v1/contacts/clear: удаляет ВСЕ контакты пользователя этого токена."""
        return self._request("DELETE", f"{CONTACTS_URL}/clear", token)

    # ---------- хелпер ----------
    def find_contacts(self, email: str, token: str) -> list[dict]:
        """Возвращает ВСЕ контакты с таким email (API допускает дубликаты)."""
        response = self.get_contacts(token)
        assert response.status_code == 200, f"GET /contacts вернул {response.status_code}: {response.text}"
        return [item for item in response.json()["contacts"] if item.get("email") == email]

    def find_contact(self, email: str, token: str) -> dict | None:
        """Первый контакт с таким email или None.

        Нужен потому, что POST /v1/contacts возвращает только message
        ("Contact was added! ID: ..."), а не JSON с полем id. Надёжнее найти контакт в списке.
        """
        found = self.find_contacts(email, token)
        return found[0] if found else None
