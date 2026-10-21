import time

from pages.login_page import LoginPage


def test_login_new_api_registered_user(driver, registered_user_via_api):
  login_page = LoginPage(driver)


  time.sleep(1.5)  # даем время базе данных зафиксировать пользователя
  login_page.login(
      registered_user_via_api.email, registered_user_via_api.password
  )
  # Если не залогинился — делаем скриншот для отладки
  if not login_page.is_logged():
      login_page.take_screenshot("empty_white_page_bug")

  assert login_page.is_logged(), "Пользователь не смог залогиниться!"