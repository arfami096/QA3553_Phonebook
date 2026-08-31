import time
import allure
import pytest
from config import VALID_EMAIL, VALID_PASSWORD


@allure.epic("Phonebook Application")
@allure.feature("User Registration")
class TestRegistration:

    @allure.story("Successful Registration")
    @allure.title("Successful registration with a new unique email and valid password")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_successful_registration(self, registration_page):
        unique_suffix = int(time.time())
        new_email = f"user_{unique_suffix}@gmail.com"

        with allure.step(f"Register new user with email: '{new_email}'"):
            registration_page.register(new_email, "Password123!")

        with allure.step("Verify user is logged in (Sign Out button is visible)"):
            assert registration_page.is_logged(), "Ошибка: регистрация не удалась (кнопка Sign Out не найдена)!"

    @allure.story("Registration Validation")
    @allure.title("Attempt to register with empty fields: {description}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "email, password, description",
        [
            ("", "", "Оба поля пустые"),
            ("", VALID_PASSWORD, "Пустой email"),
            (f"user_{int(time.time())}@gmail.com", "", "Пустой пароль"),
        ],
    )
    def test_registration_empty_fields(self, registration_page, email, password, description):
        with allure.step(f"Attempt registration with condition: {description}"):
            registration_page.register(email, password)
            try:
                registration_page.get_alert_text_and_accept()
            except Exception:
                pass

        with allure.step("Verify user is not registered / logged in"):
            assert not registration_page.is_logged(), f"Ошибка: система зарегистрировала пользователя при условии: {description}!"

    @allure.story("Email Validation")
    @allure.title("Negative email validation: {description}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "email, description",
        [
            ("testgmail.com", "T3: Нет символа @"),
            ("test@@gmail.com", "T3: Больше одного @"),
            ("@gmail.com", "T4: Нет символов до @"),
            ("test@", "T5: Нет символов после @"),
            ("тест@gmail.com", "T6: Кириллица в email"),
        ],
    )
    def test_registration_email_requirements(self, registration_page, email, description):
        with allure.step(f"Attempt registration with invalid email ({description}): '{email}'"):
            registration_page.register(email, VALID_PASSWORD)
            try:
                registration_page.get_alert_text_and_accept()
            except Exception:
                pass

        with allure.step("Verify system blocked registration with invalid email"):
            assert not registration_page.is_logged(), f"Ошибка: система пропустила невалидный email ({description})"

    @allure.story("Password Validation")
    @allure.title("Negative password validation: {description}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "password, description",
        [
            ("Password123", "T9: Нет спецсимвола"),
            ("Пароль123!", "T10: Кириллица в пароле"),
            ("password123!", "T11: Нет заглавной буквы"),
            ("PASSWORD123!", "T12: Нет строчной буквы"),
            ("Password!", "T13: Нет цифры"),
            ("Pass1!", "T14: Меньше 8 символов"),
            ("P" * 16 + "1!", "T15: Больше 15 символов"),
        ],
    )
    def test_registration_password_requirements(self, registration_page, password, description):
        unique_email = f"user_{int(time.time())}@gmail.com"

        with allure.step(f"Attempt registration with invalid password ({description})"):
            registration_page.register(unique_email, password)
            try:
                registration_page.get_alert_text_and_accept()
            except Exception:
                pass

        with allure.step("Verify system blocked registration with invalid password"):
            assert not registration_page.is_logged(), f"Ошибка: система пропустила невалидный пароль ({description})"