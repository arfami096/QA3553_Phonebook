import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.DEFAULT_TIMEOUT)

    def take_screenshot(self, file_name: str):
        """Создает папку screenshots/ и сохраняет скриншот по имени файла."""
        os.makedirs("screenshots", exist_ok=True)
        path = f"screenshots/{file_name}.png"
        self.driver.save_screenshot(path)
        print(f"\n[INFO] Скриншот сохранен: {path}")


    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def fill(self, locator, value):
        element = self.find(locator)
        element.clear()
        element.send_keys(value)

    def is_element_visible(self, locator) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False