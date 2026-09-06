import allure
import pytest
from pages.add_page import AddPage
from pages.contacts_page import ContactsPage
from utils.data_generator import DataGenerator


@allure.epic("Phonebook Application")
@allure.feature("Contact Management")
class TestRemoveContact:
  @allure.epic("Phonebook Application")
  @allure.feature("Contact Management")
  class TestRemoveContact:

    @allure.story("Contact Remove Validation")
    @allure.title("Remove contact successfully")
    @allure.severity(allure.severity_level.NORMAL)
    def test_remove_contact(self, authenticated_driver, created_contact):
      contacts_page = ContactsPage(authenticated_driver)

      # Используем контакт, который гарантированно создала фикстура
      contact = created_contact

      with allure.step(f"Find and remove the contact with phone: {contact.phone}"):
        contacts_page.select_contact_by_phone(contact.phone)
        contacts_page.remove_contact()

      with allure.step("Verify the contact is successfully removed"):
        assert not contacts_page.wait_until_contact_disappears(contact.phone), (
          "Ошибка: контакт не был удален из списка!"
        )