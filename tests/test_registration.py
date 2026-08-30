import time
import pytest
from config import VALID_EMAIL, VALID_PASSWORD



def test_successful_registration(registration_page):
    unique_suffix = int(time.time())
    new_email = f"user_{unique_suffix}@gmail.com"
    new_password = "Password123!"

    registration_page.fill_registration_form(new_email, new_password)
    registration_page.submit_registration()

    assert registration_page.is_registered(), "Ошибка: регистрация не удалась!"


def test_registration_empty_fields(registration_page):
    registration_page.submit_registration()
    try:
        registration_page.get_error_message()
    except Exception:
        pass

    assert not registration_page.is_registered(), "Ошибка: система зарегистрировала пользователя с пустыми полями!"


def test_registration_empty_email(registration_page):
    registration_page.fill_password(VALID_PASSWORD)
    registration_page.submit_registration()

    try:
        registration_page.get_error_message()
    except Exception:
        pass

    assert not registration_page.is_registered(), "Ошибка: регистрация прошла с пустым email!"


def test_registration_empty_password(registration_page):
    unique_suffix = int(time.time())
    random_email = f"user_{unique_suffix}@gmail.com"

    registration_page.fill_email(random_email)
    registration_page.submit_registration()

    try:
        registration_page.get_error_message()
    except Exception:
        pass

    assert not registration_page.is_registered(), "Ошибка: регистрация прошла с пустым паролем!"


# T1 - T6: Требования к Email при регистрации
@pytest.mark.parametrize(
    "email, description",
    [
        ("", "T1-T2: Пустой email"),
        ("testgmail.com", "T3: Нет символа @"),
        ("test@@gmail.com", "T3: Больше одного @"),
        ("@gmail.com", "T4: Нет символов до @"),
        ("test@", "T5: Нет символов после @"),
        ("тест@gmail.com", "T6: Кириллица в email"),
    ],
)
def test_registration_email_requirements(registration_page, email, description):
    registration_page.fill_registration_form(email, VALID_PASSWORD)
    registration_page.submit_registration()

    try:
        registration_page.get_error_message()
    except Exception:
        pass

    assert not registration_page.is_registered(), f"Ошибка: система пропустила невалидный email ({description})"


# T7 - T15: Требования к Password при регистрации
@pytest.mark.parametrize(
    "password, description",
    [
        ("", "T7-T8: Пустой пароль"),
        ("Password123", "T9: Нет спецсимвола [@, $, #, ^, &, *, !]"),
        ("Пароль123!", "T10: Кириллица в пароле"),
        ("password123!", "T11: Нет заглавной буквы (UpperCase)"),
        ("PASSWORD123!", "T12: Нет строчной буквы (LowCase)"),
        ("Password!", "T13: Нет цифры"),
        ("Pass1!", "T14: Меньше 8 символов"),
        ("P" * 16 + "1!", "T15: Больше 15 символов"),
    ],
)
def test_registration_password_requirements(registration_page, password, description):
    unique_suffix = int(time.time())
    unique_email = f"user_{unique_suffix}@gmail.com"

    registration_page.fill_registration_form(unique_email, password)
    registration_page.submit_registration()

    try:
        registration_page.get_error_message()
    except Exception:
        pass

    assert not registration_page.is_registered(), f"Ошибка: система пропустила невалидный пароль ({description})"

# def test_registration_touched_empty_email(registration_page):
#     # Кликаем в поле email, оставляем пустым, заполняем пароль и отправляем
#     registration_page.click(registration_page.EMAIL_INPUT)
#     registration_page.fill_password(VALID_PASSWORD)
#     registration_page.submit_registration()
#
#     alert_text = registration_page.get_alert_text_and_accept()
#     assert "Wrong email or password format" in alert_text
#
#
# def test_registration_touched_empty_password(registration_page):
#     user = DataGenerator.generate_user()
#     registration_page.fill_email(user.email)
#     registration_page.click(registration_page.PASSWORD_INPUT)
#     registration_page.submit_registration()
#
#     alert_text = registration_page.get_alert_text_and_accept()
#     assert "Wrong email or password format" in alert_text

