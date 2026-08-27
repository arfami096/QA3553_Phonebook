import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import VALID_EMAIL, VALID_PASSWORD
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage


def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", default=False, help="Run browser in headless mode"
    )


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

    browser = webdriver.Chrome(options=options)
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