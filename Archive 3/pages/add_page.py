import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class AddPage(BasePage):
    ADD_NAV_LINK = (By.CSS_SELECTOR, "a[href='/add']")
    NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Name']")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Last Name']")
    PHONE_INPUT = (By.CSS_SELECTOR, "input[placeholder='Phone']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[placeholder='email']")
    ADDRESS_INPUT = (By.CSS_SELECTOR, "input[placeholder='Address']")
    DESCRIPTION_INPUT = (By.CSS_SELECTOR, "input[placeholder='description']")
    SAVE_BTN = (By.XPATH, "//button[b[text()='Save']]")
    CONTACT_NAV_LINK = (By.CSS_SELECTOR, "[href='/contacts']")

    PHONE_ALERT_TEXT = " Phone not valid: Phone number must contain only digits! And length min 10, max 15!"
    EMAIL_ALERT_TEXT = "Email not valid: must be a well-formed email address"

    def open_contact_form(self):
        self.click(self.ADD_NAV_LINK)

    def add_new_contact(self, contact):
        self.open_contact_form()
        self.fill_contact_form(contact)
        self.submit_contact()

    def fill_name(self, name):
        self.fill(self.NAME_INPUT, name)

    def fill_last_name(self, last_name):
        self.fill(self.LAST_NAME_INPUT, last_name)

    def fill_phone(self, phone):
        self.fill(self.PHONE_INPUT, phone)

    def fill_email(self, email):
        self.fill(self.EMAIL_INPUT, email)

    def fill_address(self, address):
        self.fill(self.ADDRESS_INPUT, address)

    def fill_description(self, description):
        self.fill(self.DESCRIPTION_INPUT, description)

    def fill_contact_form(self, contact):
        self.fill_name(contact.name)
        self.fill_last_name(contact.last_name)
        self.fill_phone(contact.phone)
        self.fill_email(contact.email)
        self.fill_address(contact.address)
        self.fill_description(contact.description)

    def submit_contact(self):
        self.click(self.SAVE_BTN)

    def contact_card_visible(self, phone):
        locator = (By.XPATH, f"//h3[text()='{phone}']")
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(locator)
            )
            return element.is_displayed()
        except Exception:
            return False

    def open_contact_details(self, phone):
        locator = (By.XPATH, f"//h3[text()='{phone}']/..")
        self.click(locator)

    def is_add_button_active(self):
        add_link = self.find(self.ADD_NAV_LINK)
        return "active" in add_link.get_attribute("class")

    def open_contact_list(self):
        self.click(self.CONTACT_NAV_LINK)
        WebDriverWait(self.driver, 5 ).until(EC.url_contains("/contacts"))
        time.sleep(1)

    def contact_cards_count(self, phone):
        return len(
            self.find_elements((By.XPATH, f"//h3[text()='{phone}']"))
        )

