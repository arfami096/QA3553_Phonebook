from selenium.common import TimeoutException, NoAlertPresentException
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
    ERROR_MESSAGE = (By.XPATH, "//div[text()='Login Failed with code 401']")

    BASE_URL = "https://telranedu.web.app/"

    # def open_login_form(self):
    #     self.driver.get(self.BASE_URL)
    #     try:
    #         WebDriverWait(self.driver, 5).until(
    #             EC.element_to_be_clickable(self.LOGIN_NAV_LINK)
    #         ).click()
    #     except TimeoutException:
    #         pass

    def open_login_form(self):
        self.driver.get(self.BASE_URL)
        # Кликаем напрямую. Если элемента нет — тест упадет честно с TimeoutException
        self.click(self.LOGIN_NAV_LINK)


    def fill_email(self, email: str):
        self.fill(self.EMAIL_INPUT, email)

    def fill_password(self, password: str):
        self.fill(self.PASSWORD_INPUT, password)

    def fill_login_form(self, email: str, password: str):
        # Принудительный вывод с flush=True, чтобы pytest не прятал текст
        print(
            f"\n[UI DEBUG] Email: {email} | Password: {password}", flush=True
        )
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)

    def submit_login(self):
        self.click(self.LOGIN_BTN)

    def login(self, email, password):
        """Комплексный метод для входа в систему"""
        self.open_login_form()
        self.fill_login_form(email, password)
        self.submit_login()

    def submit_registration(self):
        self.click(self.REGISTRATION_BTN)

    def is_logged(self) -> bool:
        try:
            # Ждем появления кнопки Sign Out до 10 секунд принудительно
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.SIGN_OUT_BTN)
            )
            return True
        except TimeoutException:
            return False

    def get_error_message(self, timeout=3) -> str:
        """
        Универсальный метод: проверяет появление системного алерта,
        а если его нет — ищет элемент с ошибкой в DOM-дереве страницы.
        """
        # 1. Сначала проверяем, не появился ли системный alert
        try:
            alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert_text = alert.text
            alert.accept()  # Сразу закрываем алерт, чтобы не блокировал страницу

            return alert_text
        except (TimeoutException, NoAlertPresentException):
            pass

        # 2. Если алерта нет, ищем элемент ошибки в DOM по локатору self.ERROR_MESSAGE
        try:
            error_element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return error_element.text

        except TimeoutException:
            pass

        # 3. На крайний случай проверяем, не записан ли текст ошибки прямо в атрибут value или innerHTML (если применимо)
        try:
            element = self.driver.find_element(*self.ERROR_MESSAGE)
            text = element.text or element.get_attribute("value") or element.get_attribute("innerText")

            if text:
                return text
        except Exception:
            pass

        raise AssertionError(
            "Ошибка не найдена: ни системный alert, ни DOM-элемент ошибки (self.ERROR_MESSAGE) не обнаружены!")

    def get_alert_text(self) -> str:
        alert = self.wait.until(EC.alert_is_present())
        return alert.text

    def accept_alert(self):
        self.driver.switch_to.alert.accept()

    def logout(self):
        self.click(self.SIGN_OUT_BTN)