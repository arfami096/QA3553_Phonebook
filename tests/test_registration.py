from config import VALID_PASSWORD
from pages.registration_page import RegistrationPage
from utils.data_generator import DataGenerator


def test_registration_success(registration_page):
    # Генерируем уникального пользователя
    user = DataGenerator.generate_user()

    # Заполняем форму и отправляем
    registration_page.fill_registration_form(user.email, user.password)
    registration_page.submit_registration()

    # Проверяем успешный вход и выходим из системы
    assert registration_page.is_logged() is True
    registration_page.logout()

def test_registration_empty_fields(registration_page):
    # Оставляем поля пустыми и сразу отправляем форму
    registration_page.submit_registration()

    # Проверяем текст ошибки в алерте (или блокировку входа)
    alert_text = registration_page.get_alert_text_and_accept()
    assert "Wrong email or password format" in alert_text

def test_registration_empty_email(registration_page):
    registration_page.fill_registration_form("", "ValidPassword123!")
    registration_page.submit_registration()

    alert_text = registration_page.get_alert_text_and_accept()
    assert "Wrong email or password format" in alert_text

def test_registration_empty_password(registration_page):
    registration_page.fill_registration_form("test_user@example.com", "")
    registration_page.submit_registration()

    alert_text = registration_page.get_alert_text_and_accept()
    assert "Wrong email or password format" in alert_text

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

def test_registration_invalid_email(registration_page):
    registration_page.fill_registration_form("invalid_email.com", VALID_PASSWORD)
    registration_page.submit_registration()

    alert_text = registration_page.get_alert_text_and_accept()
    assert "Wrong email or password format" in alert_text