import time
import pytest
from config import VALID_EMAIL, VALID_PASSWORD


def test_successful_registration(registration_page):
    unique_suffix = int(time.time())
    new_email = f"user_{unique_suffix}@gmail.com"

    registration_page.register(new_email, "Password123!")

    assert registration_page.is_logged(), "Ошибка: регистрация не удалась (кнопка Sign Out не найдена)!"


@pytest.mark.parametrize(
    "email, password, description",
    [
        ("", "", "Оба поля пустые"),
        ("", VALID_PASSWORD, "Пустой email"),
        (f"user_{int(time.time())}@gmail.com", "", "Пустой пароль"),
    ],
)
def test_registration_empty_fields(registration_page, email, password, description):
    registration_page.register(email, password)

    try:
        registration_page.get_alert_text_and_accept()
    except Exception:
        pass

    assert not registration_page.is_logged(), f"Ошибка: система зарегистрировала пользователя при условии: {description}!"



# T1 - T6: ТРЕБОВАНИЯ К EMAIL
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
def test_registration_email_requirements(registration_page, email, description):
    registration_page.register(email, VALID_PASSWORD)

    try:
        registration_page.get_alert_text_and_accept()
    except Exception:
        pass

    assert not registration_page.is_logged(), f"Ошибка: система пропустила невалидный email ({description})"


# T7 - T15: ТРЕБОВАНИЯ К PASSWORD
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
def test_registration_password_requirements(registration_page, password, description):
    unique_email = f"user_{int(time.time())}@gmail.com"
    registration_page.register(unique_email, password)

    try:
        registration_page.get_alert_text_and_accept()
    except Exception:
        pass

    assert not registration_page.is_logged(), f"Ошибка: система пропустила невалидный пароль ({description})"

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

