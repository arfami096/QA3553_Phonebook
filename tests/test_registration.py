from pages.login_page import LoginPage


def test_registration_success(driver):
    login_page = LoginPage(driver)
    login_page.open_login_form()
    login_page.fill_email("poiuydswfewsdwfddsdweqwt@tyu.com")
    login_page.fill_password("Qwerty123!")
    login_page.submit_registration()

    assert login_page.is_registered() is True

    login_page.logout()

def test_registration_with_empty_fields(driver):
    login_page = LoginPage(driver)
    login_page.open_login_form()
    login_page.fill_email("")
    login_page.fill_password("")
    login_page.submit_registration()

    assert "Wrong email or password format" in login_page.get_alert_text()
    login_page.accept_alert()

def test_registration_with_empty_email_field(driver):
    login_page = LoginPage(driver)
    login_page.open_login_form()
    login_page.fill_email("")
    login_page.fill_password("Qwerty123!")
    login_page.submit_registration()

    assert "Wrong email or password format" in login_page.get_alert_text()
    login_page.accept_alert()

def test_registration_with_empty_password_field(driver):
    login_page = LoginPage(driver)
    login_page.open_login_form()
    login_page.fill_email("qwert@df.com")
    login_page.fill_password("")
    login_page.submit_registration()

    assert "Wrong email or password format" in login_page.get_alert_text()
    login_page.accept_alert()

def test_registration_with_wrong_email(driver):
    login_page = LoginPage(driver)
    login_page.open_login_form()
    login_page.fill_email("fwef.com")
    login_page.fill_password("Qwerty123!")
    login_page.submit_registration()

    assert "Wrong email or password format" in login_page.get_alert_text()
    login_page.accept_alert()

def test_login_with_wrong_password(driver):
    login_page = LoginPage(driver)
    login_page.open_login_form()
    login_page.fill_email("arfami096@icloud.com")
    login_page.fill_password("32r3")
    login_page.submit_registration()

    assert "Wrong email or password format" in login_page.get_alert_text()
    login_page.accept_alert()

def test_login_unregistered_user(driver):
    login_page = LoginPage(driver)
    login_page.open_login_form()
    login_page.fill_email("qeefe@saf.com")
    login_page.fill_password("Qwerty123!")
    login_page.submit_registration()

    assert "User already exist" in login_page.get_alert_text()
    login_page.accept_alert()

