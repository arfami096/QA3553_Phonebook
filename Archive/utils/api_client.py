from config import API_URL
import requests


class ApiClient:

  def __init__(self, base_url=API_URL):
    self.base_url = base_url
    self.session = requests.Session()
    self.session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Origin": "https://telranedu.web.app",
        "Referer": "https://telranedu.web.app/",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
    })

  def register_user(self, email, password):
    """Быстрая регистрация пользователя через API"""
    url = f"{self.base_url}/v1/user/registration/usernamepassword"
    payload = {"username": email, "password": password}
    # Используем чистый requests.post вместо self.session.post
    response = requests.post(url, json=payload, headers=self.session.headers)
    return response

  # def register_user(self, email, password):
  #   """Быстрая регистрация пользователя через API"""
  #   url = f"{self.base_url}/v1/user/registration/usernamepassword"
  #   # Пробуем передать и username, и email на всякий случай, если бэкенд ждет конкретное имя поля
  #   payload = {"username": email, "password": password}
  #   response = self.session.post(url, json=payload)
  #   return response

  def login_user(self, email, password):
    """Логин пользователя через API для получения токена"""
    url = f"{self.base_url}/v1/user/login/usernamepassword"
    payload = {"username": email, "password": password}
    response = self.session.post(url, json=payload)

    if response.status_code == 200:
      return response.json().get("token")
    return None