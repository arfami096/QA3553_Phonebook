import time
import allure
from config import VALID_EMAIL, VALID_PASSWORD


@allure.epic("Phonebook Application")
@allure.feature("Authentication")
class TestLogin:

    @allure.story("Successful Login")
    @allure.title("Successful login with valid credentials")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_successful_login(self, login_page):
        with allure.step("Log in with valid email and password"):
            login_page.login(VALID_EMAIL, VALID_PASSWORD)

        with allure.step("Verify 'Sign Out' button is visible"):
            assert login_page.is_logged(), "Кнопка 'Sign Out' не найдена — авторизация не удалась"

    @allure.story("Login Validation")
    @allure.title("Attempt to login with empty fields")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_empty_fields(self, login_page):
        with allure.step("Open login form and submit without filling fields"):
            login_page.open_login_form()
            login_page.submit_login()
            try:
                login_page.get_error_message()
            except Exception:
                pass

        with allure.step("Verify user is not logged in"):
            assert not login_page.is_logged(), "Ошибка: система пустила пользователя с пустыми полями!"

    @allure.story("Login Validation")
    @allure.title("Attempt to login with empty email field")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_empty_email(self, login_page):
        with allure.step("Open form, fill only password and submit"):
            login_page.open_login_form()
            login_page.fill_password(VALID_PASSWORD)
            login_page.submit_login()
            try:
                login_page.get_error_message()
            except Exception:
                pass

        with allure.step("Verify user is not logged in"):
            assert not login_page.is_logged(), "Ошибка: система пустила пользователя с пустым email!"

    @allure.story("Login Validation")
    @allure.title("Attempt to login with empty password field")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_empty_password(self, login_page):
        with allure.step("Open form, fill only email and submit"):
            login_page.open_login_form()
            login_page.fill_email(VALID_EMAIL)
            login_page.submit_login()
            try:
                login_page.get_error_message()
            except Exception:
                pass

        with allure.step("Verify user is not logged in"):
            assert not login_page.is_logged(), "Ошибка: система пустила пользователя с пустым паролем!"

    @allure.story("Login Validation")
    @allure.title("Attempt to login with invalid email format")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_invalid_email_format(self, login_page):
        invalid_email = "wrong_email_format"

        with allure.step(f"Attempt login with invalid email format: '{invalid_email}'"):
            login_page.login(invalid_email, VALID_PASSWORD)
            try:
                login_page.get_error_message()
            except Exception:
                pass

        with allure.step("Verify user is not logged in"):
            assert not login_page.is_logged(), "Ошибка: система пустила пользователя с неверным форматом email!"

    @allure.story("Negative Authentication")
    @allure.title("Attempt to login with incorrect password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_wrong_password(self, login_page):
        with allure.step("Attempt login with valid email and wrong password"):
            login_page.login(VALID_EMAIL, "WrongPassword999!")

        with allure.step("Verify error message and that user is not logged in"):
            error_text = login_page.get_error_message()
            assert "wrong email or password" in error_text.lower()
            assert not login_page.is_logged(), "Ошибка: пользователь вошел в систему с неверным паролем!"

    @allure.story("Negative Authentication")
    @allure.title("Attempt to login with unregistered user credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_unregistered_user(self, login_page):
        unique_suffix = int(time.time())
        unregistered_email = f"unregistered_user_{unique_suffix}@gmail.com"

        with allure.step(f"Attempt login with non-existent email: '{unregistered_email}'"):
            login_page.login(unregistered_email, "Password123!")

        with allure.step("Verify error message and that user is not logged in"):
            error_text = login_page.get_error_message()
            assert "wrong email or password" in error_text.lower()
            assert not login_page.is_logged(), "Ошибка: незарегистрированный пользователь смог войти!"