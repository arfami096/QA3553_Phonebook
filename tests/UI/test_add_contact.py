import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.add_page import AddPage
from utils.data_generator import DataGenerator
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.epic("Phonebook Application")
@allure.feature("Contact Management")
class TestAddContact:

  @allure.story("Successful Contact Creation")
  @allure.title("Add contact with valid generated data")
  @allure.severity(allure.severity_level.BLOCKER)
  def test_add_contact_positive(self, authenticated_driver):
    logger.info("Запуск теста: успешное создание контакта с валидными данными")
    add_page = AddPage(authenticated_driver)
    contact = DataGenerator.generate_contact()
    logger.info(
        f"Сгенерирован тестовый контакт: {contact.name} {contact.lastName} |"
        f" {contact.phone}"
    )

    with allure.step("Fill and submit the new contact form"):
      logger.info("Заполняем форму нового контакта и отправляем")
      add_page.add_new_contact(contact)

    with allure.step("Verify user is redirected to the contacts list"):
      logger.info(
          "Проверяем редирект пользователя на страницу списка контактов (/contacts)"
      )
      WebDriverWait(authenticated_driver, 5).until(
          EC.url_contains("/contacts")
      )
      assert "contacts" in authenticated_driver.current_url
      logger.info("Тест успешно пройден: редирект подтвержден")

  @allure.story("Optional Fields Handling")
  @allure.title("Add contact with empty description field")
  @allure.severity(allure.severity_level.NORMAL)
  def test_add_contact_with_empty_description(self, authenticated_driver):
    logger.info("Запуск теста: создание контакта с пустым описанием")
    add_page = AddPage(authenticated_driver)
    contact = DataGenerator.generate_contact(description="")

    with allure.step("Create contact with empty description"):
      logger.info("Заполняем форму с пустым описанием и отправляем")
      add_page.add_new_contact(contact)

    with allure.step("Verify successful redirection to contacts list"):
      logger.info("Проверяем успешный редирект на список контактов")
      WebDriverWait(authenticated_driver, 5).until(
          EC.url_contains("/contacts")
      )
      assert "contacts" in authenticated_driver.current_url
      logger.info("Тест успешно пройден")

  @allure.story("Optional Fields Handling")
  @allure.title("Add contact with numbers and symbols in description")
  @allure.severity(allure.severity_level.NORMAL)
  def test_add_contact_description_with_numbers_and_symbols(
      self, authenticated_driver
  ):
    logger.info(
        "Запуск теста: создание контакта с цифрами и спецсимволами в описании"
    )
    add_page = AddPage(authenticated_driver)
    contact = DataGenerator.generate_contact(
        description="Test description! 123 #@$"
    )

    with allure.step("Create contact with complex symbols in description"):
      logger.info("Заполняем форму и отправляем контакт")
      add_page.add_new_contact(contact)

    with allure.step("Verify successful redirection to contacts list"):
      logger.info("Проверяем успешный редирект на список контактов")
      WebDriverWait(authenticated_driver, 5).until(
          EC.url_contains("/contacts")
      )
      assert "contacts" in authenticated_driver.current_url
      logger.info("Тест успешно пройден")

  @allure.story("Form Validation")
  @allure.title("Attempt to submit completely empty contact form")
  @allure.severity(allure.severity_level.CRITICAL)
  def test_add_contact_all_fields_empty(self, authenticated_driver):
    logger.info("Запуск негативного теста: отправка полностью пустой формы")
    add_page = AddPage(authenticated_driver)

    with allure.step("Open contact form and submit without filling fields"):
      logger.info("Открываем форму и пытаемся отправить без заполнения полей")
      add_page.open_contact_form()
      try:
        add_page.submit_contact()
      except Exception as e:
        logger.info(f"Перехвачено ожидаемое исключение/действие при сабмите: {e}")

    with allure.step("Verify that user remains on the add contact page"):
      logger.info("Проверяем, что пользователь остался на странице /add")
      assert "/add" in authenticated_driver.current_url, (
          "Ошибка: полностью пустая форма позволила себя отправить!"
      )
      logger.info("Тест успешно пройден: форма заблокирована")

  @allure.story("Field Validation")
  @allure.title(
      "Test text fields with valid variations: {field_name} -> {valid_value}"
  )
  @allure.severity(allure.severity_level.NORMAL)
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
          ("address", "St. John's, #5"),
      ],
  )
  def test_contact_text_fields_valid_variations(
      self, authenticated_driver, field_name, valid_value
  ):
    logger.info(
        f"Запуск параметризованного теста: проверка валидного значения"
        f" '{valid_value}' для поля '{field_name}'"
    )
    add_page = AddPage(authenticated_driver)
    overrides = {field_name: valid_value}
    contact = DataGenerator.generate_contact(**overrides)

    with allure.step(f"Add contact with valid {field_name}: '{valid_value}'"):
      logger.info(f"Добавляем контакт с {field_name} = {valid_value}")
      add_page.add_new_contact(contact)

    with allure.step("Verify successful creation and redirect"):
      logger.info("Проверяем успешное создание и редирект")
      WebDriverWait(authenticated_driver, 5).until(
          EC.url_contains("/contacts")
      )
      assert "contacts" in authenticated_driver.current_url, (
          f"Ошибка: поле '{field_name}' отклонило валидное значение"
          f" '{valid_value}'!"
      )
      logger.info("Валидация значения прошла успешно")

  @allure.story("Field Validation")
  @allure.title(
      "Negative validation for {field_name} with value '{invalid_value}'"
  )
  @pytest.mark.parametrize(
      "field_name, invalid_value, expected_behavior, expected_alert",
      [
          pytest.param("name", "", "stay_on_page", None),
          pytest.param("last_name", "", "stay_on_page", None),
          pytest.param("phone", "", "stay_on_page", None),
          pytest.param("email", "", "stay_on_page", None),
          pytest.param("address", "", "stay_on_page", None),
          pytest.param(
              "email", "userexample.com", "alert", AddPage.EMAIL_ALERT_TEXT
          ),
          pytest.param(
              "email", "user@@example.com", "alert", AddPage.EMAIL_ALERT_TEXT
          ),
          pytest.param(
              "email", "@domain.com", "alert", AddPage.EMAIL_ALERT_TEXT
          ),
          pytest.param("email", "user@", "alert", AddPage.EMAIL_ALERT_TEXT),
          pytest.param(
              "email",
              "пользователь@domain.com",
              "alert",
              AddPage.EMAIL_ALERT_TEXT,
              marks=pytest.mark.xfail(
                  reason=(
                      "Bug: Application accepts Cyrillic characters in email"
                      " field"
                  )
              ),
          ),
          pytest.param("phone", "abc_phone", "alert", AddPage.PHONE_ALERT_TEXT),
          pytest.param("phone", "12345", "alert", AddPage.PHONE_ALERT_TEXT),
          pytest.param(
              "phone", "1234567890123456", "alert", AddPage.PHONE_ALERT_TEXT
          ),
          pytest.param("phone", "12345-67890", "alert", AddPage.PHONE_ALERT_TEXT),
      ],
  )
  def test_add_contact_negative_validation(
      self,
      authenticated_driver,
      field_name,
      invalid_value,
      expected_behavior,
      expected_alert,
  ):
    allure.dynamic.severity(allure.severity_level.CRITICAL)
    logger.info(
        f"Запуск негативного теста: поле '{field_name}' со значением"
        f" '{invalid_value}' (ожидается: {expected_behavior})"
    )

    add_contact_page = AddPage(authenticated_driver)
    overrides = {field_name: invalid_value}
    contact = DataGenerator.generate_contact(**overrides)

    with allure.step(
        f"Fill form with invalid data into {field_name}: '{invalid_value}'"
    ):
      add_contact_page.open_contact_form()
      add_contact_page.fill_contact_form(contact)
      try:
        add_contact_page.submit_contact()
      except Exception as e:
        logger.info(f"Действие сабмита вызвало исключение: {e}")

    if expected_behavior == "stay_on_page":
      with allure.step("Verify that form blocks submission and stays on /add"):
        logger.info("Проверяем, что форма заблокирована и осталась на /add")
        assert "/add" in authenticated_driver.current_url, (
            f"Ошибка: при пустом поле '{field_name}' форма отправилась, хотя"
            " должна была остаться на /add!"
        )

    elif expected_behavior == "alert":
      with allure.step(
          f"Verify warning alert appears with text containing '{expected_alert}'"
      ):
        logger.info("Ожидаем появления браузерного алерта с ошибкой")
        wait = WebDriverWait(authenticated_driver, 5)
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        logger.info(f"Перехвачен текст алерта: '{alert_text}'")
        alert.accept()

        assert expected_alert in alert_text, (
            f"Ожидался алерт с текстом '{expected_alert}', но получено:"
            f" '{alert_text}'"
        )
    logger.info("Негативный тест успешно пройден")

  @allure.story("Duplicate Control")
  @allure.title("Prevent creating contact with duplicate email")
  @allure.severity(allure.severity_level.CRITICAL)
  def test_add_contact_duplicate_email(self, authenticated_driver):
    logger.info("Запуск теста: проверка блокировки дубликата email")
    add_page = AddPage(authenticated_driver)
    contact = DataGenerator.generate_contact()

    with allure.step("Create the initial contact"):
      logger.info(f"Создаем базовый контакт с email: {contact.email}")
      add_page.add_new_contact(contact)
      WebDriverWait(authenticated_driver, 5).until(EC.url_contains("/contacts"))

    with allure.step("Attempt to create another contact with the same email"):
      logger.info("Пробуем создать второй контакт с тем же email")
      add_page.open_contact_form()
      duplicate_contact = DataGenerator.generate_contact(email=contact.email)
      add_page.fill_contact_form(duplicate_contact)
      try:
        add_page.submit_contact()
      except Exception as e:
        logger.info(f"Сабмит дубликата вызвал исключение: {e}")

    with allure.step("Verify system rejects duplicate email"):
      logger.info("Проверяем, что система заблокировала дубликат")
      assert (
          "/add" in authenticated_driver.current_url
          or EC.alert_is_present()(authenticated_driver)
      )
      logger.info("Тест на дубликат email пройден")

  @allure.story("Duplicate Control")
  @allure.title("Prevent creating contact with duplicate phone number")
  @allure.severity(allure.severity_level.CRITICAL)
  def test_add_contact_duplicate_phone(self, authenticated_driver):
    logger.info("Запуск теста: проверка блокировки дубликата номера телефона")
    add_page = AddPage(authenticated_driver)
    first_contact = DataGenerator.generate_contact()

    with allure.step("Create the initial contact"):
      logger.info(f"Создаем базовый контакт с телефоном: {first_contact.phone}")
      add_page.add_new_contact(first_contact)
      WebDriverWait(authenticated_driver, 5).until(EC.url_contains("/contacts"))

    with allure.step(
        "Attempt to create another contact with the same phone number"
    ):
      logger.info("Пробуем создать второй контакт с тем же номером телефона")
      add_page.open_contact_form()
      duplicate_contact = DataGenerator.generate_contact(
          phone=first_contact.phone
      )
      add_page.fill_contact_form(duplicate_contact)
      try:
        add_page.submit_contact()
      except Exception as e:
        logger.info(f"Сабмит дубликата телефона вызвал исключение: {e}")

    with allure.step("Verify system rejects duplicate phone number"):
      logger.info("Проверяем отказ системы в создании дубликата телефона")
      assert (
          "/add" in authenticated_driver.current_url
          or EC.alert_is_present()(authenticated_driver)
      ), (
          "Ошибка: приложение позволило создать второй контакт с уже"
          " существующим номером телефона!"
      )
      logger.info("Тест на дубликат телефона успешно пройден")