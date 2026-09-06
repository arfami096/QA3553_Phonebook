import allure
import pytest
from pages.add_page import AddPage
from pages.contacts_page import ContactsPage
from utils.data_generator import DataGenerator


@allure.epic("Phonebook Application")
@allure.feature("Contact Management")
class TestUpdateContact:

    @allure.story("Contact Update Validation")
    @allure.title("Update Name invalid: {invalid_name}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(reason="Bug: Update form allows clicking Save on empty name instead of blocking it or showing an alert")
    @pytest.mark.parametrize("invalid_name", ["", "    "])
    def test_update_name_invalid_keeps_save_button_disabled(self, authenticated_driver, invalid_name):
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
    @allure.severity(allure.severity_level.CRITICAL)
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
            contacts_page.select_contact_by_phone(contact.phone)

        with allure.step(f"Ждем обновления и проверяем, что имя '{valid_name}' находится на первой строке карточки"):
            assert contacts_page.wait_until_card_text_contains(valid_name), \
                f"Имя '{valid_name}' не отобразилось в карточке после сохранения"
            card_text = contacts_page.get_card_text()
            lines = [line.strip() for line in card_text.splitlines() if line.strip()]
            assert valid_name in lines[0], \
                f"Ожидалось, что имя '{valid_name}' будет на 1-й строке (индекс 0), но получили строки: {lines}"

    @allure.story("Contact Update Validation")
    @allure.title("Update Last Name invalid: {invalid_last_name}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(reason="Bug: Update form allows clicking Save on empty last name instead of blocking it or showing an alert")
    @pytest.mark.parametrize("invalid_last_name", ["", "    "])
    def test_update_last_name_invalid_keeps_save_button_disabled(self, authenticated_driver, invalid_last_name):
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
    @allure.severity(allure.severity_level.CRITICAL)
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
            contacts_page.select_contact_by_phone(contact.phone)

        with allure.step(f"Ждем обновления и проверяем, что фамилия '{valid_last_name}' находится на первой строке карточки"):
            assert contacts_page.wait_until_card_text_contains(valid_last_name), \
                f"Фамилия '{valid_last_name}' не отобразилась в карточке после сохранения"
            card_text = contacts_page.get_card_text()
            lines = [line.strip() for line in card_text.splitlines() if line.strip()]
            assert valid_last_name in lines[0], \
                f"Ожидалось, что фамилия '{valid_last_name}' будет на 1-й строке (индекс 0), но получили строки: {lines}"

    @allure.story("Contact Update Validation")
    @allure.title("Update Email invalid: {invalid_email}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.xfail(reason="Bug: Application allows saving contact with empty or invalid email during update")
    @pytest.mark.parametrize("invalid_email", [
        "", "testmail.com", "test@@mail.com", "@mail.com", "test@", "тест@mail.com"
    ])
    def test_update_email_invalid_keeps_save_button_disabled(self, authenticated_driver, invalid_email):
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
    @allure.title("Update Email valid: {valid_email}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("valid_email", ["new_mail@gmail.com", "user.name@domain.co", "test+tag@mail.org"])
    def test_update_email_valid(self, authenticated_driver, valid_email):
        """Позитивный тест для проверки валидных email-адресов."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Создаем тестовый контакт"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Открываем редактирование и вводим валидный email: '{valid_email}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_email(valid_email)

        with allure.step("Проверяем активность кнопки Save и сохраняем"):
            assert contacts_page.is_save_button_enabled(), "Кнопка Save должна быть активной"
            contacts_page.submit_contact()
            contacts_page.select_contact_by_phone(contact.phone)

        with allure.step(f"Ждем обновления и проверяем, что email '{valid_email}' находится на строке с индексом 2"):
            assert contacts_page.wait_until_card_text_contains(valid_email), \
                f"Email '{valid_email}' не отобразился в карточке после сохранения"
            card_text = contacts_page.get_card_text()
            lines = [line.strip() for line in card_text.splitlines() if line.strip()]
            assert valid_email in lines[2], \
                f"Ожидалось, что email '{valid_email}' будет на 3-й строке (индекс 2), но получили строки: {lines}"

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
    @pytest.mark.xfail(reason="Bug: Update form allows clicking Save on empty address instead of blocking it")
    @pytest.mark.parametrize("invalid_address", ["", "    "])
    def test_update_address_invalid_keeps_save_button_disabled(self, authenticated_driver, invalid_address):
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
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("valid_address", ["Main St 12", "Street #5/B", "X"])
    def test_update_address_valid(self, authenticated_driver, valid_address):
        """T73, T74: Numbers and special characters allowed in Address."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        # Приводим адрес к одной строке на случай переносов
        clean_address = " ".join(valid_address.splitlines()).strip()

        with allure.step("Создаем тестовый контакт"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Открываем редактирование и вводим валидный адрес: '{clean_address}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_address(clean_address)

        with allure.step("Проверяем активность кнопки Save и сохраняем"):
            assert contacts_page.is_save_button_enabled(), "Кнопка Save должна быть активной"
            contacts_page.submit_contact()
            contacts_page.select_contact_by_phone(contact.phone)

        with allure.step(f"Ждем обновления и проверяем, что адрес '{clean_address}' находится на строке с индексом 3"):
            assert contacts_page.wait_until_card_text_contains(clean_address), \
                f"Адрес '{clean_address}' не отобразился в карточке после сохранения"
            card_text = contacts_page.get_card_text()
            lines = [line.strip() for line in card_text.splitlines() if line.strip()]
            assert clean_address in lines[3], \
                f"Ожидалось, что адрес '{clean_address}' будет на 4-й строке (индекс 3), но получили строки: {lines}"
    @allure.story("Contact Update Validation")
    @allure.title("Update Phone invalid: {invalid_phone}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.xfail(reason="Bug: Update form allows clicking Save on invalid phone instead of blocking it")
    @pytest.mark.parametrize("invalid_phone", [
        "", "123456789", "1234567890123456", "12345-67890", "12345abc901"
    ])
    def test_update_phone_invalid_keeps_save_button_disabled(self, authenticated_driver, invalid_phone):
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
    @allure.title("Update Phone valid: {valid_phone}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("valid_phone", ["9998887766", "123456789012"])
    def test_update_phone_valid(self, authenticated_driver, valid_phone):
        """Позитивный тест для проверки валидных телефонов."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Создаем тестовый контакт"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Открываем редактирование и вводим новый валидный телефон: '{valid_phone}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_phone(valid_phone)

        with allure.step("Сохраняем изменения"):
            assert contacts_page.is_save_button_enabled(), "Кнопка Save должна быть активной"
            contacts_page.submit_contact()
            contacts_page.select_contact_by_phone(valid_phone)

        with allure.step(f"Ждем обновления и проверяем, что телефон '{valid_phone}' находится на строке с индексом 1"):
            assert contacts_page.wait_until_card_text_contains(valid_phone), \
                f"Телефон '{valid_phone}' не отобразился в карточке после сохранения"
            card_text = contacts_page.get_card_text()
            lines = [line.strip() for line in card_text.splitlines() if line.strip()]
            assert valid_phone in lines[1], \
                f"Ожидалось, что телефон '{valid_phone}' будет на 2-й строке (индекс 1), но получили строки: {lines}"

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
    @allure.title("Validation for Description valid")
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
            contacts_page.select_contact_by_phone(contact.phone)

        # Если описание не пустое, дожидаемся его появления и проверяем на ожидаемой строке (индекс 4)
        if valid_description.strip():
            with allure.step(f"Ждем обновления и проверяем, что описание '{valid_description}' находится на строке с индексом 4"):
                assert contacts_page.wait_until_card_text_contains(valid_description), \
                    f"Описание '{valid_description}' не отобразилось в карточке после сохранения"
                card_text = contacts_page.get_card_text()
                lines = [line.strip() for line in card_text.splitlines() if line.strip()]
                assert valid_description in lines[4], \
                    f"Ожидалось, что описание '{valid_description}' будет на 5-й строке (индекс 4), но получили строки: {lines}"