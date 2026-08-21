from pages.login_page import LoginPage

VALID_EMAIL = "arfami096@gmail.com"
VALID_PASSWORD = "Jamalungma08!"


def test_login_success(driver):
    login_page = LoginPage(driver)
    login_page.open_login_form()
    login_page.fill_email(VALID_EMAIL)
    login_page.fill_password(VALID_PASSWORD)
    login_page.submit_login()

    assert login_page.is_logged() is True


def test_login_with_wrong_email(driver):
    login_page = LoginPage(driver)
    login_page.open_login_form()
    login_page.fill_email("fwef.com")
    login_page.fill_password(VALID_PASSWORD)
    login_page.submit_login()

    assert login_page.get_alert_text() == "Wrong email or password"
    login_page.accept_alert()


def test_login_with_wrong_password(driver):
    login_page = LoginPage(driver)
    login_page.open_login_form()
    login_page.fill_email(VALID_EMAIL)
    login_page.fill_password("32r3")
    login_page.submit_login()

    assert login_page.get_alert_text() == "Wrong email or password"
    login_page.accept_alert()


def test_login_unregistered_user(driver):
    login_page = LoginPage(driver)
    login_page.open_login_form()
    login_page.fill_email(VALID_EMAIL)
    login_page.fill_password(VALID_PASSWORD)
    login_page.submit_login()

    assert login_page.get_alert_text() == "Wrong email or password"
    login_page.accept_alert()
