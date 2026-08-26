from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage


class LoginPage(BasePage):
    LOGIN_NAV_LINK = (By.CSS_SELECTOR, "[href='/login']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[name='password']")
    LOGIN_BTN = (By.XPATH, "//button[text()='Login']")
    REGISTRATION_BTN = (By.XPATH, "//button[text()='Registration']")
    SIGN_OUT_BTN = (By.XPATH, "//*[text()='Sign Out']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")

    BASE_URL = "https://telranedu.web.app/"

    def open_login_form(self):
        self.driver.get(self.BASE_URL)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.LOGIN_NAV_LINK)
            ).click()
        except TimeoutException:
            pass

    def fill_email(self, email: str):
        self.fill(self.EMAIL_INPUT, email)

    def fill_password(self, password: str):
        self.fill(self.PASSWORD_INPUT, password)

    def fill_login_form(self, email: str, password: str):
        self.fill_email(email)
        self.fill_password(password)

    def submit_login(self):
        self.click(self.LOGIN_BTN)

    def submit_registration(self):
        self.click(self.REGISTRATION_BTN)

    def is_logged(self) -> bool:
        return self.is_element_visible(self.SIGN_OUT_BTN)

    def get_error_message(self) -> str:
        return self.driver.find_element(*self.ERROR_MESSAGE).text

    def get_alert_text(self) -> str:
        alert = self.wait.until(EC.alert_is_present())
        return alert.text

    def accept_alert(self):
        self.driver.switch_to.alert.accept()

    def logout(self):
        self.click(self.SIGN_OUT_BTN)