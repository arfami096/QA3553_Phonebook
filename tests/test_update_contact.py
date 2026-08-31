import allure
import pytest
from pages.add_page import AddPage
from pages.contacts_page import ContactsPage
from utils.data_generator import DataGenerator


@allure.epic("Phonebook Application")
@allure.feature("Contact Management")
class TestUpdateContact:

    @allure.story("Contact Update")
    @allure.title("Successfully update contact email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_contact_email(self, authenticated_driver):
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Шаг подготовки: создаем контакт стандартным способом"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step("Сам тест: находим созданный контакт по его телефону и меняем email"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_email("new_mail@gmail.com")
            contacts_page.submit_contact()

    @allure.story("Contact Update Validation")
    @allure.title("Update Name invalid: {invalid_name}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(reason="Bug: Update form allows clicking Save on empty name instead of blocking it or showing an alert")
    @pytest.mark.parametrize("invalid_name", ["", "    "])
    def test_update_name_invalid_shows_disabled_save(self, authenticated_driver, invalid_name):
        """T54, T55, T58: Name is required, must not be blank, min 1 symbol."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Создаем тестовый контакт"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Выбираем контакт, открываем редактирование и вводим невалидное имя: '{invalid_name}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_name(invalid_name)

        with allure.step("Проверяем, что кнопка Save неактивна"):
            assert not contacts_page.is_save_button_enabled(), "Кнопка Save должна быть неактивной при пустом имени"

    @allure.story("Contact Update Validation")
    @allure.title("Update Name valid: {valid_name}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("valid_name", ["John123", "Anna-Maria!", "A"])
    def test_update_name_valid(self, authenticated_driver, valid_name):
        """T56, T57: Numbers and special characters are allowed in Name."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Создаем тестовый контакт"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Выбираем контакт, открываем редактирование и вводим валидное имя: '{valid_name}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_name(valid_name)

        with allure.step("Проверяем активность кнопки Save и сохраняем"):
            assert contacts_page.is_save_button_enabled(), "Кнопка Save должна быть активной"
            contacts_page.submit_contact()

    @allure.story("Contact Update Validation")
    @allure.title("Update Last Name invalid: {invalid_last_name}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(reason="Bug: Update form allows clicking Save on empty last name instead of blocking it or showing an alert")
    @pytest.mark.parametrize("invalid_last_name", ["", "    "])
    def test_update_last_name_invalid(self, authenticated_driver, invalid_last_name):
        """T59, T60, T63: Last Name is required, must not be blank, min 1 symbol."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Создаем тестовый контакт"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Открываем редактирование и вводим невалидную фамилию: '{invalid_last_name}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_last_name(invalid_last_name)

        with allure.step("Проверяем неактивность кнопки Save"):
            assert not contacts_page.is_save_button_enabled(), "Кнопка Save должна быть неактивной при пустой фамилии"

    @allure.story("Contact Update Validation")
    @allure.title("Update Last Name valid: {valid_last_name}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("valid_last_name", ["Smith99", "O'Connor#", "B"])
    def test_update_last_name_valid(self, authenticated_driver, valid_last_name):
        """T61, T62: Numbers and special characters allowed in Last Name."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Создаем тестовый контакт"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Открываем редактирование и вводим валидную фамилию: '{valid_last_name}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_last_name(valid_last_name)

        with allure.step("Проверяем активность кнопки Save и сохраняем"):
            assert contacts_page.is_save_button_enabled(), "Кнопка Save должна быть активной"
            contacts_page.submit_contact()

    @allure.story("Contact Update Validation")
    @allure.title("Update Email invalid: {invalid_email}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.xfail(reason="Bug: Application allows saving contact with empty or invalid email during update")
    @pytest.mark.parametrize("invalid_email", [
        "",  # T64, T65: required / blank
        "testmail.com",  # T66: no @
        "test@@mail.com",  # T66: more than one @
        "@mail.com",  # T67: no chars before @
        "test@",  # T68: no chars after @
        "тест@mail.com",  # T69: non-English characters
    ])
    def test_update_email_invalid(self, authenticated_driver, invalid_email):
        """T64-T69: Email format validation."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Создаем тестовый контакт"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Открываем редактирование и вводим невалидный email: '{invalid_email}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_email(invalid_email)

        with allure.step("Проверяем неактивность кнопки Save"):
            assert not contacts_page.is_save_button_enabled(), "Кнопка Save должна быть неактивной при невалидном мейле"

    @allure.story("Contact Update Validation")
    @allure.title("Update Email duplicate check")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(reason="Bug: Update form allows saving duplicate emails (T70)")
    def test_update_email_duplicate(self, authenticated_driver):
        """T70: Email should not be repeated with existing contact."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Создаем тестовый контакт"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        existing_email = "already_exists@mail.com"

        with allure.step(f"Пытаемся обновить email на существующий дубликат: '{existing_email}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_email(existing_email)
            contacts_page.submit_contact()

        with allure.step("Проверяем обработку ошибки/алерта"):
            assert contacts_page.handle_error_or_alert(), "Система должна была отклонить дубликат email!"

    @allure.story("Contact Update Validation")
    @allure.title("Update Address invalid: {invalid_address}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(reason="Bug: Update form allows clicking Save on empty adress instead of blocking it or showing an alert")
    @pytest.mark.parametrize("invalid_address", ["", "    "])
    def test_update_address_invalid(self, authenticated_driver, invalid_address):
        """T71, T72, T75: Address is required, must not be blank."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Создаем тестовый контакт"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Открываем редактирование и вводим невалидный адрес: '{invalid_address}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_address(invalid_address)

        with allure.step("Проверяем неактивность кнопки Save"):
            assert not contacts_page.is_save_button_enabled(), "Кнопка Save должна быть неактивной при пустом адресе"

    @allure.story("Contact Update Validation")
    @allure.title("Update Address valid: {valid_address}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("valid_address", ["Main St 12", "Street #5/B", "X"])
    def test_update_address_valid(self, authenticated_driver, valid_address):
        """T73, T74: Numbers and special characters allowed in Address."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Создаем тестовый контакт"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Открываем редактирование и вводим валидный адрес: '{valid_address}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_address(valid_address)

        with allure.step("Проверяем активность кнопки Save и сохраняем"):
            assert contacts_page.is_save_button_enabled(), "Кнопка Save должна быть активной"
            contacts_page.submit_contact()

    @allure.story("Contact Update Validation")
    @allure.title("Update Phone invalid: {invalid_phone}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.xfail(reason="Bug: Update form allows clicking Save on invalid phone instead of blocking it or showing an alert")
    @pytest.mark.parametrize("invalid_phone", [
        "",  # T76, T77: required / blank
        "123456789",  # T79: min 10 symbols (9 digits here)
        "1234567890123456",  # T80: max 15 symbols (16 digits here)
        "12345-67890",  # T81: special chars not allowed
        "12345abc901",  # T82: letters not allowed
    ])
    def test_update_phone_invalid(self, authenticated_driver, invalid_phone):
        """T76-T82: Phone number validation (digits only, length 10-15)."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Создаем тестовый контакт"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Открываем редактирование и вводим невалидный телефон: '{invalid_phone}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_phone(invalid_phone)

        with allure.step("Проверяем неактивность кнопки Save"):
            assert not contacts_page.is_save_button_enabled()

    @allure.story("Contact Update Validation")
    @allure.title("Update Phone duplicate check")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(reason="Bug: Application allows updating phone to a duplicate of an existing contact")
    def test_update_phone_duplicate(self, authenticated_driver):
        """T83: Phone should not repeat an existing contact's phone."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Создаем тестовый контакт"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        existing_phone = "0530000000"

        with allure.step(f"Пытаемся обновить телефон на дубликат: '{existing_phone}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_phone(existing_phone)
            contacts_page.submit_contact()

        with allure.step("Проверяем отклонение дубликата системой"):
            assert contacts_page.handle_error_or_alert(), "Система должна была отклонить дубликат телефона!"

    @allure.story("Contact Update Validation")
    @allure.title("Update Description valid: {valid_description}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("valid_description", ["", "Description 123", "Notes #!@"])
    def test_update_description_valid(self, authenticated_driver, valid_description):
        """T84-T86: Description is not required, supports numbers and special characters."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Создаем тестовый контакт"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Открываем редактирование и вводим описание: '{valid_description}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_description(valid_description)

        with allure.step("Проверяем активность кнопки Save и сохраняем"):
            assert contacts_page.is_save_button_enabled(), "Кнопка Save должна быть активной"
            contacts_page.submit_contact()