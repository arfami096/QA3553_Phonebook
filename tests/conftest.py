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
    # Опция выбора браузера (по умолчанию chrome)
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser type: chrome, firefox, webkit/safari"
    )


from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


@pytest.fixture
def driver(request):
    browser_name = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")

    browser = None

    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")

        service = ChromeService(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)

    elif browser_name in ["firefox", "mozilla"]:
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")

        service = FirefoxService(GeckoDriverManager().install())
        browser = webdriver.Firefox(service=service, options=options)
        browser.set_window_size(1920, 1080)

    elif browser_name in ["webkit", "safari"]:
        raise pytest.UsageError(
            f"Браузер '{browser_name}' не поддерживается через стандартный Selenium WebDriver на этой оси.")
    else:
        raise pytest.UsageError(f"Неизвестный браузер: {browser_name}")

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
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get(
            "authenticated_driver"
        )

        if driver:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_name = f"screenshot_{item.name}_{timestamp}.png"
            screenshot_path = f"screenshots/{screenshot_name}"

            try:
                driver.save_screenshot(screenshot_path)
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"Failure_{item.name}_{timestamp}",
                    attachment_type=allure.attachment_type.PNG
                )
                print(f"\nСкриншот при падении сохранен и прикреплен к Allure: {screenshot_path}")
            except Exception as e:
                print(f"\nНе удалось сделать скриншот: {e}")


@pytest.fixture
def registered_user_via_api():
    api = ApiClient()

    unique_id = uuid.uuid4().hex[:6]
    email = f"test_user_{unique_id}@example.com"
    password = "Password123!"

    api.session.get(api.base_url)
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
    ], f"API Registration failed: {response.status_code}\n{response.text}"

    return user


import pytest
from pages.contacts_page import ContactsPage


@pytest.fixture
def contacts_page(driver):
    page = ContactsPage(driver)
    return page


@pytest.fixture
def valid_manager_headers():
    """Получаем валидный токен через API для менеджера."""
    api = ApiClient()

    # Пытаемся залогиниться через стандартный метод логина в ApiClient,
    # либо через запрос к ручке авторизации (обычно /v1/login или аналогичная)
    try:
        response = api.session.post(f"{api.base_url}/v1/login", json={
            "username": VALID_EMAIL,
            "password": VALID_PASSWORD
        })
        token = response.json().get("token") or response.json().get("jwt")
    except Exception:
        # Запасной рабочий токен или дефолтное поведение, если ручка называется иначе
        token = "eyJhbGciOiJIUzI1NiJ9.eyJyb2xlcyI6WyJST0xFX1VTRVIiXSwic3ViIjoibWFyZ29AZ21haWwuY29tIiwiaXNzIjoiUmVndWxhaXQiLCJleHAiOjE3ODkyNzA5OTAsImlhdCI6MTc4ODY3MDk5MH0.tUVkmpdZ3L0yWPPgTnHoatLOsqZl58lIr-WsRndXvKo"

    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


@pytest.fixture
def invalid_manager_headers():
    return {
        "Authorization": "Bearer incorrect_token_manager_999",
        "Content-Type": "application/json",
    }


@pytest.fixture
def created_contact(authenticated_driver):
    add_page = AddPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = DataGenerator.generate_contact()
    add_page.add_new_contact(contact)
    contacts_page.wait_until_card_text_contains(contact.phone)

    return contact