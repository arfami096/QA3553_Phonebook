import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    browser = webdriver.Chrome()
    browser.get("https://telranedu.web.app/home")

    yield browser

    browser.quit()