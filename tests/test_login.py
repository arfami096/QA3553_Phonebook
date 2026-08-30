import time
from config import VALID_EMAIL, VALID_PASSWORD


def test_successful_login(login_page):
    login_page.login(VALID_EMAIL, VALID_PASSWORD)
    assert login_page.is_logged(), "Кнопка 'Sign Out' не найдена — авторизация не удалась"


def test_login_empty_fields(login_page):
    login_page.open_login_form()
    login_page.submit_login()

    try:
        login_page.get_error_message()
    except Exception:
        pass

    assert not login_page.is_logged(), "Ошибка: система пустила пользователя с пустыми полями!"


def test_login_empty_email(login_page):
    login_page.open_login_form()
    login_page.fill_password(VALID_PASSWORD)
    login_page.submit_login()

    try:
        login_page.get_error_message()
    except Exception:
        pass

    assert not login_page.is_logged(), "Ошибка: система пустила пользователя с пустым email!"


def test_login_empty_password(login_page):
    login_page.open_login_form()
    login_page.fill_email(VALID_EMAIL)
    login_page.submit_login()

    try:
        login_page.get_error_message()
    except Exception:
        pass

    assert not login_page.is_logged(), "Ошибка: система пустила пользователя с пустым паролем!"


def test_login_with_invalid_email_format(login_page):
    invalid_email = "wrong_email_format"
    login_page.login(invalid_email, VALID_PASSWORD)

    try:
        login_page.get_error_message()
    except Exception:
        pass

    assert not login_page.is_logged(), "Ошибка: система пустила пользователя с неверным форматом email!"


def test_login_with_wrong_password(login_page):
    login_page.login(VALID_EMAIL, "WrongPassword999!")

    error_text = login_page.get_error_message()
    assert "wrong email or password" in error_text.lower()
    assert not login_page.is_logged(), "Ошибка: пользователь вошел в систему с неверным паролем!"


def test_login_unregistered_user(login_page):
    unique_suffix = int(time.time())
    unregistered_email = f"unregistered_user_{unique_suffix}@gmail.com"

    login_page.login(unregistered_email, "Password123!")

    error_text = login_page.get_error_message()
    assert "wrong email or password" in error_text.lower()
    assert not login_page.is_logged(), "Ошибка: незарегистрированный пользователь смог войти!"

# def test_login_touched_empty_email(login_page):
#     # Кликаем в поле email, но ничего не вводим, затем кликаем в другое место (или сразу сабмитим)
#     login_page.click(login_page.EMAIL_INPUT)
#     login_page.fill_password(VALID_PASSWORD)
#     login_page.submit_login()
#
#     assert not login_page.is_logged(), "Ошибка: пустил с пустым, но 'тронутым' email!"

# def test_login_touched_empty_password(login_page):
#     login_page.fill_email(VALID_EMAIL)
#     login_page.click(login_page.PASSWORD_INPUT)
#     login_page.submit_login()
#
#     assert not login_page.is_logged(), "Ошибка: пустил с пустым, но 'тронутым' email!"


