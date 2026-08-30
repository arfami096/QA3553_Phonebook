import time
from config import VALID_EMAIL, VALID_PASSWORD


def test_successful_login(login_page):
    login_page.fill_login_form(VALID_EMAIL, VALID_PASSWORD)
    login_page.submit_login()
    assert login_page.is_logged(), "Кнопка 'Sign Out' не найдена — авторизация не удалась"

def test_login_empty_fields(login_page):
    login_page.submit_login()
    try:
        login_page.get_error_message()
    except Exception:
        pass

    assert not login_page.is_logged(), "Ошибка: система пустила пользователя с пустыми полями!"


def test_login_empty_email(login_page):
    login_page.fill_password(VALID_PASSWORD)
    login_page.submit_login()
    try:
        login_page.get_error_message()
    except Exception:
        pass

    assert not login_page.is_logged(), "Ошибка: система пустила пользователя с пустым email!"


def test_login_empty_password(login_page):
    login_page.fill_email(VALID_EMAIL)
    login_page.submit_login()
    try:
        login_page.get_error_message()
    except Exception:
        pass

    assert not login_page.is_logged(), "Ошибка: система пустила пользователя с пустым паролем!"


def test_login_with_invalid_email_format(login_page):
    invalid_email = "wrong_email_format"
    login_page.fill_login_form(invalid_email, VALID_PASSWORD)
    login_page.submit_login()

    try:
        login_page.get_error_message()
    except Exception:
        pass

    assert not login_page.is_logged(), "Ошибка: система пустила пользователя с неверным форматом email!"


def test_login_with_wrong_password(login_page):
    wrong_password = "WrongPassword999!"
    login_page.fill_login_form(VALID_EMAIL, wrong_password)
    login_page.submit_login()

    error_text = login_page.get_error_message()
    assert "fail" in error_text.lower() or "401" in error_text or "error" in error_text.lower()
    assert not login_page.is_logged(), "Ошибка: пользователь вошел в систему с неверным паролем!"


def test_login_unregistered_user(login_page):
    unique_suffix = int(time.time())
    unregistered_email = f"unregistered_user_{unique_suffix}@gmail.com"
    random_password = "Password123!"

    login_page.fill_login_form(unregistered_email, random_password)
    login_page.submit_login()

    error_text = login_page.get_error_message()
    assert "fail" in error_text.lower() or "401" in error_text or "error" in error_text.lower()
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


