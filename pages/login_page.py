from selenium.webdriver.support import expected_conditions as EC

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class LoginPage:


    LOGIN_NAV_LINK = (By.CSS_SELECTOR, "[href='/login']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[name='password']")
    LOGIN_BTN = (By.XPATH, "//button[text()='Login']")
    SIGN_OUT_BTN = (By.XPATH, "//*[text()='Sign Out']")
    REGISTRATION_BTN = (By.XPATH, "//button[text()='Registration']")
    CONTACTS_NAV_LINK = (By.CSS_SELECTOR, "a[href='/contacts']")

    def __init__(self, driver):
        self.driver = driver



    def open_login_form(self):
        self.driver.find_element(*self.LOGIN_NAV_LINK).click()

    def fill_email(self, email):
        self.driver.find_element(*self.EMAIL_INPUT).clear()
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)

    def fill_password(self, password):
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def submit_login(self):
        self.driver.find_element(*self.LOGIN_BTN).click()

    def submit_registration(self):
        self.driver.find_element(*self.REGISTRATION_BTN).click()

    # def is_logged(self):
    #     try:
    #         self.driver.find_element(*self.SIGN_OUT_BTN)
    #         return True
    #     except NoSuchElementException:
    #         return False

    def is_logged(self):
        try:
            WebDriverWait(self.driver, timeout=5).until(
                expected_conditions.visibility_of_element_located(self.SIGN_OUT_BTN))
            return True
        except TimeoutException:
            return False

    def get_alert_text(self):
        alert = WebDriverWait(self.driver, timeout=5).until(expected_conditions.alert_is_present())

        return alert.text

    def accept_alert(self):
        self.driver.switch_to.alert.accept()

    def is_registered(self):
        try:
            WebDriverWait(self.driver, timeout=10).until(
                expected_conditions.visibility_of_element_located(self.CONTACTS_NAV_LINK))
            return True
        except TimeoutException:
            return False
    def logout(self):
        self.driver.find_element(*self.SIGN_OUT_BTN).click()