import datetime
import uuid
from types import SimpleNamespace
from config import VALID_EMAIL, VALID_PASSWORD
from pages.add_page import AddPage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from utils.api_client import ApiClient
import pytest
import allure

from utils.data_generator import DataGenerator


def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", default=False, help="Run browser in headless mode"
    )

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver(request):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

    # Инициализация драйвера через менеджер
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)

    browser.set_page_load_timeout(10)
    yield browser

    try:
        browser.quit()
    except Exception:
        pass

@pytest.fixture
def authenticated_driver(driver):
    """Фикстура, которая автоматически логинит пользователя перед тестом."""
    login_page = LoginPage(driver)
    login_page.open_login_form()
    login_page.fill_login_form(VALID_EMAIL, VALID_PASSWORD)
    login_page.submit_login()
    return driver

@pytest.fixture
def login_page(driver):
    page = LoginPage(driver)
    page.open_login_form()
    return page

@pytest.fixture
def registration_page(driver):
    page = RegistrationPage(driver)
    page.open_registration_form()
    return page



@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Получаем результат выполнения теста
    outcome = yield
    report = outcome.get_result()

    # Проверяем, что тест упал именно на этапе выполнения (call)
    if report.when == "call" and report.failed:
        # Пытаемся достать фикстуру драйвера из теста
        driver = item.funcargs.get("driver") or item.funcargs.get(
            "authenticated_driver"
        )

        if driver:
            # Генерируем уникальное имя файла с таймстампом
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_name = f"screenshot_{item.name}_{timestamp}.png"

            # Путь, куда сохранится файл
            screenshot_path = f"screenshots/{screenshot_name}"

            try:
                # 1. Сохраняем локально на диск (как было)
                driver.save_screenshot(screenshot_path)

                # 2. Прикрепляем скриншот в отчет Allure для облака
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"Failure_{item.name}_{timestamp}",
                    attachment_type=allure.attachment_type.PNG
                )

                print(f"\nСкриншот при падении сохранен и прикреплен к Allure: {screenshot_path}")
            except Exception as e:
                print(f"\nНе удалось сделать скриншот: {e}")

# @pytest.fixture
# def registered_user_via_api():
#   api = ApiClient()
#   user = DataGenerator.generate_user()
#
#   response = api.register_user(user.email, user.password)
#   print(f"[API RESPONSE STATUS]: {response.status_code}, BODY: {response.text}")
#
#   # Добавили flush=True
#   print(f"\n[DEBUG API] Status Code: {response.status_code}", flush=True)
#   print(f"[DEBUG API] Response text: {response.text}", flush=True)
#   print(
#       f"[DEBUG API] Email: {user.email} | Password: {user.password}",
#       flush=True,
#   )
#
#   assert response.status_code in [
#       200,
#       201,
#   ], f"API Registration failed: {response.status_code} - {response.text}"
#
#   return user



@pytest.fixture
def registered_user_via_api():
  api = ApiClient()

  # Используем встроенный uuid для генерации уникального хвоста почты
  unique_id = uuid.uuid4().hex[:6]
  email = f"test_user_{unique_id}@example.com"
  password = "Password123!"

  # «Знакомимся» с сайтом, чтобы сервер выдал куки/сессию
  api.session.get(api.base_url)

  # Отправляем запрос на регистрацию
  response = api.register_user(email, password)

  response = api.register_user(email, password)

  user = SimpleNamespace(email=email, password=password)

  print(f"[API RESPONSE STATUS]: {response.status_code}, BODY: {response.text}")
  print(f"\n[DEBUG API] Status Code: {response.status_code}", flush=True)
  print(f"[DEBUG API] Response text: {response.text}", flush=True)
  print(
      f"[DEBUG API] Email: {user.email} | Password: {user.password}",
      flush=True,
  )

  assert response.status_code in [
      200,
      201,
  ], f"API Registration failed: {response.status_code} - {response.text}"

  return user

import pytest
from pages.contacts_page import ContactsPage

@pytest.fixture
def contacts_page(driver):
    page = ContactsPage(driver)
    return page



@pytest.fixture
def valid_manager_headers():
  # Настоящий валидный токен (можно вынести в config или переменную окружения)
  token = ("eyJhbGciOiJIUzI1NiJ9.eyJyb2xlcyI6WyJST0xFX1VTRVIiXSwic3ViIjoibWFyZ29AZ21haWwuY29tIiwiaXNzIjoiUmVndWxhaXQiLCJleHAiOjE3ODkyNzA5OTAsImlhdCI6MTc4ODY3MDk5MH0.tUVkmpdZ3L0yWPPgTnHoatLOsqZl58lIr-WsRndXvKo")
  return {
      "Authorization": f"Bearer {token}",
      "Content-Type": "application/json",
  }


@pytest.fixture
def invalid_manager_headers():
  # Неверный токен, но тоже с префиксом Bearer, чтобы сервер дошел до валидации токена
  return {
      "Authorization": "Bearer incorrect_token_manager_999",
      "Content-Type": "application/json",
  }

@pytest.fixture
def created_contact(authenticated_driver):
  """Фикстура для подготовки данных: создает уникальный контакт перед тестом

  и гарантирует, что в UI есть с чем работать.
  """
  add_page = AddPage(authenticated_driver)
  contacts_page = ContactsPage(authenticated_driver)

  contact = DataGenerator.generate_contact()

  # Прекондишн: создаем контакт через UI (или через API для скорости)
  add_page.add_new_contact(contact)
  contacts_page.wait_until_card_text_contains(contact.phone)

  # Возвращаем объект контакта, чтобы тест мог им воспользоваться
  return contact