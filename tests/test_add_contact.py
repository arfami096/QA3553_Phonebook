from models.contact import Contact
from pages.add_page import AddPage
from utils.data_generator import DataGenerator


def test_add_contact_success_all_fields(authenticated_driver):
    add_page = AddPage(authenticated_driver)

    contact = DataGenerator.generate_contact()

    # Если для конкретного теста нужно переопределить какое-то поле (например, имя),
    # можно сделать так:
    # contact.name = "Anna"

    add_page.open_contact_form()
    add_page.fill_contact_form(contact)
    add_page.submit_contact()

    assert add_page.contact_card_visible(contact.phone), "Карточка добавленного контакта не найдена на странице!"