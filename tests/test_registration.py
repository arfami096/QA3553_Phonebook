from pages.registration_page import RegistrationPage
from utils.data_generator import DataGenerator


def test_registration_success(driver):
    registration_page = RegistrationPage(driver)
    user = DataGenerator.generate_user()

    registration_page.open_registration_form()
    registration_page.fill_registration_form(user.email, user.password)
    registration_page.submit_registration()

    assert registration_page.is_logged() is True
    registration_page.logout()


def test_registration_invalid_email(driver):
    registration_page = RegistrationPage(driver)

    registration_page.open_registration_form()
    registration_page.fill_registration_form("invalid_email.com", "Password123!")
    registration_page.submit_registration()

    # Берем текст ошибки и сразу закрываем alert за одно действие
    alert_text = registration_page.get_alert_text_and_accept()
    assert "Wrong email or password format" in alert_text