from selenium.common import TimeoutException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage


class RegistrationPage(BasePage):

    LOGIN_NAV_LINK = (By.CSS_SELECTOR, "a[href='/login']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    REGISTRATION_BTN = (By.XPATH, "//button[@name='registration']")
    SIGN_OUT_BTN = (By.XPATH, "//button[text()='Sign Out']")

    BASE_URL = "https://telranedu.web.app/"


    def open_registration_form(self):
        self.driver.get(self.BASE_URL)
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.LOGIN_NAV_LINK)
            ).click()
        except TimeoutException:
            pass

    def fill_registration_form(self, email, password):
        # Заполнение email
        email_el = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.EMAIL_INPUT)
        )
        email_el.clear()
        email_el.send_keys(email)

        # Заполнение пароля
        pass_el = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.PASSWORD_INPUT)
        )
        pass_el.clear()
        pass_el.send_keys(password)

    def submit_registration(self):
        btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.REGISTRATION_BTN)
        )
        btn.click()

    def get_alert_text_and_accept(self, timeout=5) -> str:
        """Ждет alert, забирает его текст и сразу закрывает."""
        alert = WebDriverWait(self.driver, timeout).until(
            EC.alert_is_present()
        )
        text = alert.text
        alert.accept()
        return text

    def handle_alert_if_present(self, timeout=2):
        """Безопасно гасит alert с явным ожиданием, если он появился."""
        try:
            alert = WebDriverWait(self.driver, timeout).until(
                EC.alert_is_present()
            )
            alert.accept()
        except TimeoutException:
            pass

    def is_logged(self) -> bool:
        # Гасим alert об успешном входе/регистрации, если он появился
        self.handle_alert_if_present(timeout=2)
        try:
            WebDriverWait(self.driver, timeout=5).until(
                EC.visibility_of_element_located(self.SIGN_OUT_BTN)
            )
            return True
        except TimeoutException:
            return False

    def logout(self):
        # Дополнительная страховка перед кликом выхода
        self.handle_alert_if_present(timeout=1)
        btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.SIGN_OUT_BTN)
        )
        btn.click()
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.LOGIN_NAV_LINK)
        )