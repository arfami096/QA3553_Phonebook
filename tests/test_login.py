import time
from config import VALID_EMAIL, VALID_PASSWORD


def test_successful_login(login_page):

    # Заполняем форму данными из конфига (.env)
    login_page.fill_login_form(VALID_EMAIL, VALID_PASSWORD)

    login_page.submit_login()
    assert login_page.is_logged(), "Кнопка 'Sign Out' не найдена — авторизация не удалась"
    # assert False, "Специально валим тест для проверки скриншота!"


def test_login_empty_fields(login_page):
    login_page.submit_login()

    # Проверяем, что вход не произошел
    assert not login_page.is_logged(), "Ошибка: система пустила пользователя с пустыми полями!"


def test_login_empty_email(login_page):
    login_page.fill_password(VALID_PASSWORD)
    login_page.submit_login()

    assert not login_page.is_logged(), "Ошибка: система пустила пользователя с пустым email!"

def test_login_empty_password(login_page):
    login_page.fill_email(VALID_EMAIL)
    login_page.submit_login()

    assert not login_page.is_logged(), "Ошибка: система пустила пользователя с пустым паролем!"


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


def test_login_with_invalid_email(login_page):

    invalid_email = "wrong_user_9999_gmail.com"
    login_page.fill_login_form(invalid_email, VALID_PASSWORD)

    login_page.submit_login()

    assert not login_page.is_logged(), "Ошибка: система пустила пользователя с несуществующим email!"


def test_login_with_invalid_password(login_page):

    wrong_password = "wrongpassword123!"
    login_page.fill_login_form(VALID_EMAIL, wrong_password)

    login_page.submit_login()

    assert not login_page.is_logged(), "Ошибка: пользователь вошел в систему с неверным паролем!"

    error_text = login_page.get_error_message()
    assert "failed" in error_text.lower() or "401" in error_text, f"Ожидался текст ошибки, но получено: {error_text}"


def test_login_unregistered_user(login_page):
    # Генерируем уникальные данные случайного незарегистрированного пользователя
    unique_suffix = int(time.time())
    unregistered_email = f"unregistered_user_{unique_suffix}@gmail.com"
    random_password = "Password123!"

    # Пытаемся войти под ними
    login_page.fill_login_form(unregistered_email, random_password)
    login_page.submit_login()

    # Обязательно считываем и закрываем появившийся alert с ошибкой
    error_text = login_page.get_error_message()
    assert "wrong email or password" in error_text.lower() or "401" in error_text

    # Проверяем, что система заблокировала вход
    assert not login_page.is_logged(), "Ошибка: незарегистрированный пользователь смог войти!"
