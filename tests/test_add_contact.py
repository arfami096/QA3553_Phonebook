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
        ("email", "not-an-email-format", "alert", AddPage.EMAIL_ALERT_TEXT),
        ("phone", "abc_phone", "alert", AddPage.PHONE_ALERT_TEXT),
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
        assert "/add" in authenticated_driver.current_url, (
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