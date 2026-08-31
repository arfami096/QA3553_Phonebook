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

        with allure.step("Create initial contact for testing update"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step("Select contact, open edit form and update email"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_email("new_mail@gmail.com")
            contacts_page.submit_contact()

    @allure.story("Contact Update Validation")
    @allure.title("Update Name with invalid value '{invalid_name}'")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(reason="Bug: Update form allows clicking Save on empty name instead of blocking it or showing an alert")
    @pytest.mark.parametrize("invalid_name", ["", "   "])
    def test_update_name_invalid_shows_disabled_save(self, authenticated_driver, invalid_name):
        """T54, T55, T58: Name is required, must not be blank, min 1 symbol."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Create initial contact"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Open edit form and enter invalid name: '{invalid_name}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_name(invalid_name)

        with allure.step("Verify that Save button is disabled"):
            assert not contacts_page.is_save_button_enabled(), "Кнопка Save должна быть неактивной при пустом имени"

    @allure.story("Contact Update Validation")
    @allure.title("Update Name with valid value '{valid_name}'")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("valid_name", ["John123", "Anna-Maria!", "A"])
    def test_update_name_valid(self, authenticated_driver, valid_name):
        """T56, T57: Numbers and special characters are allowed in Name."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Create initial contact"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Open edit form and update name to: '{valid_name}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_name(valid_name)

        with allure.step("Verify Save button is active and submit"):
            assert contacts_page.is_save_button_enabled(), "Кнопка Save должна быть активной"
            contacts_page.submit_contact()

    @allure.story("Contact Update Validation")
    @allure.title("Update Last Name with invalid value '{invalid_last_name}'")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(reason="Bug: Update form allows clicking Save on empty last name instead of blocking it or showing an alert")
    @pytest.mark.parametrize("invalid_last_name", ["", "   "])
    def test_update_last_name_invalid(self, authenticated_driver, invalid_last_name):
        """T59, T60, T63: Last Name is required, must not be blank, min 1 symbol."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Create initial contact"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Open edit form and enter invalid last name: '{invalid_last_name}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_last_name(invalid_last_name)

        with allure.step("Verify Save button is disabled"):
            assert not contacts_page.is_save_button_enabled(), "Кнопка Save должна быть неактивной при пустой фамилии"

    @allure.story("Contact Update Validation")
    @allure.title("Update Last Name with valid value '{valid_last_name}'")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("valid_last_name", ["Smith99", "O'Connor#", "B"])
    def test_update_last_name_valid(self, authenticated_driver, valid_last_name):
        """T61, T62: Numbers and special characters allowed in Last Name."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Create initial contact"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Open edit form and update last name to: '{valid_last_name}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_last_name(valid_last_name)

        with allure.step("Verify Save button is active and submit"):
            assert contacts_page.is_save_button_enabled(), "Кнопка Save должна быть активной"
            contacts_page.submit_contact()

    @allure.story("Contact Update Validation")
    @allure.title("Update Email with invalid value '{invalid_email}'")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.xfail(reason="Bug: Update form allows saving contact with empty or invalid email during update")
    @pytest.mark.parametrize("invalid_email", [
        "", "testmail.com", "test@@mail.com", "@mail.com", "test@", "тест@mail.com",
    ])
    def test_update_email_invalid(self, authenticated_driver, invalid_email):
        """T64-T69: Email format validation."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Create initial contact"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Open edit form and enter invalid email: '{invalid_email}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_email(invalid_email)

        with allure.step("Verify Save button is disabled"):
            assert not contacts_page.is_save_button_enabled(), "Кнопка Save должна быть неактивной при невалидном мейле"

    @allure.story("Contact Update Validation")
    @allure.title("Prevent updating email to a duplicate value")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(reason="Bug: Update form allows saving duplicate emails (T70)")
    def test_update_email_duplicate(self, authenticated_driver):
        """T70: Email should not be repeated with existing contact."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Create initial contact"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        existing_email = "already_exists@mail.com"

        with allure.step(f"Attempt to update email to duplicate value: '{existing_email}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_email(existing_email)
            contacts_page.submit_contact()

        with allure.step("Verify system rejects duplicate email"):
            assert contacts_page.handle_error_or_alert(), "Система должна была отклонить дубликат email!"

    @allure.story("Contact Update Validation")
    @allure.title("Update Address with invalid value '{invalid_address}'")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(reason="Bug: Update form allows clicking Save on empty adress instead of blocking it or showing an alert")
    @pytest.mark.parametrize("invalid_address", ["", "   "])
    def test_update_address_invalid(self, authenticated_driver, invalid_address):
        """T71, T72, T75: Address is required, must not be blank."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Create initial contact"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Open edit form and enter invalid address: '{invalid_address}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_address(invalid_address)

        with allure.step("Verify Save button is disabled"):
            assert not contacts_page.is_save_button_enabled(), "Кнопка Save должна быть неактивной при пустом адресе"

    @allure.story("Contact Update Validation")
    @allure.title("Update Address with valid value '{valid_address}'")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("valid_address", ["Main St 12", "Street #5/B", "X"])
    def test_update_address_valid(self, authenticated_driver, valid_address):
        """T73, T74: Numbers and special characters allowed in Address."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Create initial contact"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Open edit form and update address to: '{valid_address}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_address(valid_address)

        with allure.step("Verify Save button is active and submit"):
            assert contacts_page.is_save_button_enabled(), "Кнопка Save должна быть активной"
            contacts_page.submit_contact()

    @allure.story("Contact Update Validation")
    @allure.title("Update Phone with invalid value '{invalid_phone}'")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.xfail(reason="Bug: Update form allows clicking Save on invalid phone instead of blocking it or showing an alert")
    @pytest.mark.parametrize("invalid_phone", [
        "", "123456789", "1234567890123456", "12345-67890", "12345abc901",
    ])
    def test_update_phone_invalid(self, authenticated_driver, invalid_phone):
        """T76-T82: Phone number validation (digits only, length 10-15)."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Create initial contact"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Open edit form and enter invalid phone: '{invalid_phone}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_phone(invalid_phone)

        with allure.step("Verify Save button is disabled"):
            assert not contacts_page.is_save_button_enabled()

    @allure.story("Contact Update Validation")
    @allure.title("Prevent updating phone to a duplicate value")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(reason="Bug: Application allows updating phone to a duplicate of an existing contact")
    def test_update_phone_duplicate(self, authenticated_driver):
        """T83: Phone should not repeat an existing contact's phone."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Create initial contact"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        existing_phone = "0530000000"

        with allure.step(f"Attempt to update phone to duplicate value: '{existing_phone}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_phone(existing_phone)
            contacts_page.submit_contact()

        with allure.step("Verify system rejects duplicate phone"):
            assert contacts_page.handle_error_or_alert(), "Система должна была отклонить дубликат телефона!"

    @allure.story("Contact Update Validation")
    @allure.title("Update Description with valid value '{valid_description}'")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("valid_description", ["", "Description 123", "Notes #!@"])
    def test_update_description_valid(self, authenticated_driver, valid_description):
        """T84-T86: Description is not required, supports numbers and special characters."""
        add_page = AddPage(authenticated_driver)
        contacts_page = ContactsPage(authenticated_driver)

        with allure.step("Create initial contact"):
            contact = DataGenerator.generate_contact()
            add_page.add_new_contact(contact)

        with allure.step(f"Open edit form and update description to: '{valid_description}'"):
            contacts_page.select_contact_by_phone(contact.phone)
            contacts_page.click_edit()
            contacts_page.update_description(valid_description)

        with allure.step("Verify Save button is active and submit"):
            assert contacts_page.is_save_button_enabled(), "Кнопка Save должна быть активной"
            contacts_page.submit_contact()