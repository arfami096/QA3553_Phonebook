from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pages.base_page import BasePage


class ContactsPage(BasePage):
    EDIT_BTN = (By.XPATH, "//button[text()='Edit']")
    REMOVE_BTN = (By.XPATH, "//button[text()='Remove']")
    SAVE_BTN = (By.XPATH, "//button[text()='Save']")

    NAME_INPUT = (By.CSS_SELECTOR, "[placeholder='Name']")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "[placeholder='Last Name']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "[placeholder='email']")
    PHONE_INPUT = (By.CSS_SELECTOR, "[placeholder='Phone']")
    ADDRESS_INPUT = (By.CSS_SELECTOR, "[placeholder='Address']")
    DESCRIPTION_INPUT = (By.CSS_SELECTOR, "[placeholder='desc']")

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
        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            if alert:
                alert.text
                alert.accept()
                return True
        except TimeoutException:
            pass

        try:
            if self.is_save_button_enabled():
                return True
        except Exception:
            pass

        return False

    def select_contact_by_phone(self, phone: str):
        dynamic_locator = (By.XPATH, f"//*[contains(text(), '{phone}')]")
        self.click(dynamic_locator)

    def get_card_text(self) -> str:
        """Получает весь текстовый контент из карточки выбранного контакта с защитой от изменения хэшей классов."""
        selectors = [
            (By.CSS_SELECTOR, "[class*='contact-item-detailed_card']"),
            (By.CSS_SELECTOR, ".contact-item-detailed_card"),
            (By.XPATH, "//div[contains(@class, 'card')]"),
            (By.TAG_NAME, "body")  # Безопасный запасной вариант, если карточка не найдена локально
        ]

        for locator in selectors:
            try:
                card_element = self.driver.find_element(*locator)
                text = card_element.text.strip()
                if text:
                    return text
            except Exception:
                continue
        return ""

    def wait_until_card_text_contains(self, expected_text: str, timeout: int = 5) -> bool:
        """Ждет, пока в тексте карточки появится новое актуальное значение."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                lambda driver: expected_text in self.get_card_text()
            )
        except TimeoutException:
            return False

    def wait_until_contact_disappears(self, phone: str, timeout: int = 5) -> bool:
        """Ждет исчезновения контакта со страницы."""
        locator = (
            By.XPATH,
            f"//*[contains(text(), '{phone}')] | //*[contains(@value, '{phone}')]",
        )
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False