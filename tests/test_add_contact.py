from selenium.webdriver.support import expected_conditions as EC

import pytest
from selenium.webdriver.support.wait import WebDriverWait

from pages.add_page import AddPage
from utils.data_generator import DataGenerator


def test_add_contact_positive(authenticated_driver):
  add_page = AddPage(authenticated_driver)
  contact = DataGenerator.generate_contact()

  add_page.add_new_contact(contact)

  WebDriverWait(authenticated_driver, 5).until(
      EC.url_contains("/contacts")
  )

  assert "contacts" in authenticated_driver.current_url


def test_add_contact_with_empty_description(authenticated_driver):
  add_page = AddPage(authenticated_driver)
  contact = DataGenerator.generate_contact(description="")

  add_page.add_new_contact(contact)

  WebDriverWait(authenticated_driver, 5).until(
      EC.url_contains("/contacts")
  )

  assert "contacts" in authenticated_driver.current_url


def test_add_contact_description_with_numbers_and_symbols(authenticated_driver):
    add_page = AddPage(authenticated_driver)
    contact = DataGenerator.generate_contact(description="Test description! 123 #@$")

    add_page.add_new_contact(contact)

    WebDriverWait(authenticated_driver, 5).until(
        EC.url_contains("/contacts")
    )
    assert "contacts" in authenticated_driver.current_url

def test_add_contact_all_fields_empty(authenticated_driver):
    add_page = AddPage(authenticated_driver)
    add_page.open_contact_form()

    try:
        add_page.submit_contact()
    except Exception:
        # Если кнопка заблокирована и клик вызвал исключение — это ожидаемо
        pass

    assert "/add" in authenticated_driver.current_url, (
        "Ошибка: полностью пустая форма позволила себя отправить!"
      )


@pytest.mark.parametrize(
    "field_name, valid_value",
    [
        ("name", "A"),
        ("name", "John2"),
        ("name", "O'Connor"),

        ("last_name", "B"),
        ("last_name", "Smith-Jr"),
        ("last_name", "Agent007"),

        ("address", "X"),
        ("address", "Apt 4B"),
        ("address", "St. John's, #5")
    ],
)

def test_contact_text_fields_valid_variations(authenticated_driver, field_name, valid_value):
    add_page = AddPage(authenticated_driver)

    overrides = {field_name: valid_value}
    contact = DataGenerator.generate_contact(**overrides)

    add_page.add_new_contact(contact)

    WebDriverWait(authenticated_driver, 5).until(
        EC.url_contains("/contacts")
    )

    assert "contacts" in authenticated_driver.current_url, (
        f"Ошибка: поле '{field_name}' отклонило валидное значение '{valid_value}'!"
    )

@pytest.mark.parametrize(
    "field_name, invalid_value, expected_behavior, expected_alert",
    [
        # Пустые обязательные поля (ожидаем, что останемся на /add)
        ("name", "", "stay_on_page", None),
        ("last_name", "", "stay_on_page", None),
        ("phone", "", "stay_on_page", None),
        ("email", "", "stay_on_page", None),
        ("address", "", "stay_on_page", None),
        # Некорректные форматы (ожидаем системный алерт)
        ("email", "userexample.com", "alert", AddPage.EMAIL_ALERT_TEXT),
        ("email", "user@@example.com", "alert", AddPage.EMAIL_ALERT_TEXT),
        ("email", "@domain.com", "alert", AddPage.EMAIL_ALERT_TEXT),
        ("email", "user@", "alert", AddPage.EMAIL_ALERT_TEXT),
        pytest.param(
            "email",
            "пользователь@domain.com",
            "alert",
            AddPage.EMAIL_ALERT_TEXT,
            marks=pytest.mark.xfail(reason="Bug: Application accepts Cyrillic characters in email field")
        ),

        ("phone", "abc_phone", "alert", AddPage.PHONE_ALERT_TEXT),
        ("phone", "12345", "alert", AddPage.PHONE_ALERT_TEXT),
        ("phone", "1234567890123456", "alert", AddPage.PHONE_ALERT_TEXT),
        ("phone", "12345-67890", "alert", AddPage.PHONE_ALERT_TEXT),
    ],
)
def test_add_contact_negative_validation(
        authenticated_driver,
        field_name,
        invalid_value,
        expected_behavior,
        expected_alert,
):
    add_contact_page = AddPage(authenticated_driver)

    overrides = {field_name: invalid_value}
    contact = DataGenerator.generate_contact(**overrides)

    add_contact_page.open_contact_form()
    add_contact_page.fill_contact_form(contact)

    # Кликаем на сохранение
    try:
        add_contact_page.submit_contact()
    except Exception:
        # Если из-за валидации или блокировки кнопки клик вызвал тайм-аут —
        # для пустых полей это ожидаемое поведение, идем дальше проверять URL
        pass

    if expected_behavior == "stay_on_page":
        assert "/ad" in authenticated_driver.current_url, (
            f"Ошибка: при пустом поле '{field_name}' форма отправилась, хотя должна"
            " была остаться на /add!"
        )

    elif expected_behavior == "alert":
        wait = WebDriverWait(authenticated_driver, 5)
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()

        assert (
                expected_alert in alert_text
        ), f"Ожидался алерт с текстом '{expected_alert}', но получено: '{alert_text}'"


def test_add_contact_duplicate_email(authenticated_driver):
    add_page = AddPage(authenticated_driver)
    contact = DataGenerator.generate_contact()

    add_page.add_new_contact(contact)
    WebDriverWait(authenticated_driver, 5).until(EC.url_contains("/contacts"))

    add_page.open_contact_form()
    duplicate_contact = DataGenerator.generate_contact(email=contact.email)
    add_page.fill_contact_form(duplicate_contact)

    try:
        add_page.submit_contact()
    except Exception:
        pass

    assert "/add" in authenticated_driver.current_url or EC.alert_is_present()(authenticated_driver)


def test_add_contact_duplicate_phone(authenticated_driver):
    add_page = AddPage(authenticated_driver)

    first_contact = DataGenerator.generate_contact()
    add_page.add_new_contact(first_contact)
    WebDriverWait(authenticated_driver, 5).until(EC.url_contains("/contacts"))

    add_page.open_contact_form()

    duplicate_contact = DataGenerator.generate_contact(phone=first_contact.phone)
    add_page.fill_contact_form(duplicate_contact)

    try:
        add_page.submit_contact()
    except Exception:
        pass

    assert "/add" in authenticated_driver.current_url or EC.alert_is_present()(authenticated_driver), (
        "Ошибка: приложение позволило создать второй контакт с уже существующим номером телефона!"
    )