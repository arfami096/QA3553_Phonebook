import time
from models.contact import Contact
from pages.add_page import AddPage


def test_add_contact_success_all_fields(authenticated_driver):
    add_page = AddPage(authenticated_driver)


    random_digits = str(time.time_ns())[-7:]
    timestamp = int(time.time())

    contact = Contact(
        name="Anna",
        last_name="Test",
        phone=f"053{random_digits}",
        email=f"user_{timestamp}@gmail.com",
        address="efgaegewg",
        description="QA lesson contact"
    )

    add_page.open_contact_form()
    add_page.fill_contact_form(contact)
    add_page.submit_contact()

    assert add_page.contact_card_visible(contact.phone), "Карточка добавленного контакта не найдена на странице!"