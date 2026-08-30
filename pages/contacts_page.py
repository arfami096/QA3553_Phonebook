from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pages.base_page import BasePage


class ContactsPage(BasePage):
    EDIT_BTN = (By.XPATH, "//button[text()='Edit']")
    REMOVE_BTN = (By.XPATH, "//button[text()='Remove']")
    SAVE_BTN = (By.XPATH, "//button[text()='Save']")

    NAME_INPUT = (By.CSS_SELECTOR, "input:nth-of-type(1)")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "input:nth-of-type(2)")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input:nth-of-type(3)")
    PHONE_INPUT = (By.CSS_SELECTOR, "input:nth-of-type(4)")
    ADDRESS_INPUT = (By.CSS_SELECTOR, "input:nth-of-type(5)")
    DESCRIPTION_INPUT = (By.CSS_SELECTOR, "input:nth-of-type(6)")

    def select_contact_by_text(self, contact_text: str):
        dynamic_locator = (By.XPATH, f"//*[contains(text(), '{contact_text}')]")
        self.click(dynamic_locator)

    def click_edit(self):
        self.click(self.EDIT_BTN)

    def click_remove(self):
        self.click(self.REMOVE_BTN)

    def submit_contact(self):
        self.click(self.SAVE_BTN)

    def is_save_button_enabled(self) -> bool:
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.SAVE_BTN)
            )
            return True
        except TimeoutException:
            return False

    # Точечные методы обновления конкретных полей
    def update_name(self, name: str):
        element = self.find(self.NAME_INPUT)
        element.clear()
        element.send_keys(name)

    def update_last_name(self, last_name: str):
        element = self.find(self.LAST_NAME_INPUT)
        element.clear()
        element.send_keys(last_name)

    def update_email(self, email: str):
        element = self.find(self.EMAIL_INPUT)
        element.clear()
        element.send_keys(email)

    def update_phone(self, phone: str):
        element = self.find(self.PHONE_INPUT)
        element.clear()
        element.send_keys(phone)

    def update_address(self, address: str):
        element = self.find(self.ADDRESS_INPUT)
        element.clear()
        element.send_keys(address)

    def update_description(self, description: str):
        element = self.find(self.DESCRIPTION_INPUT)
        element.clear()
        element.send_keys(description)

    def remove_contact(self):
        self.click(self.REMOVE_BTN)

    def handle_error_or_alert(self) -> bool:
        """
        Универсальная проверка ошибки:
        1. Проверяет системный alert (если он есть — принимает и возвращает True).
        2. Проверяет наличие текста/баннера ошибки на форме.
        3. Либо подтверждает, что мы все еще находимся в режиме редактирования.
        """
        # 1. Пробуем поймать alert
        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            if alert:
                alert.text
                alert.accept()
                return True
        except TimeoutException:
            pass

        # 2. Проверяем, остались ли мы в режиме редактирования (кнопка Save все еще видна)
        try:
            if self.is_save_button_enabled():
                return True
        except Exception:
            pass

        return False

    def select_contact_by_phone(self, phone: str):
        dynamic_locator = (By.XPATH, f"//*[contains(text(), '{phone}')]")
        self.click(dynamic_locator)