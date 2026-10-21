class StorageHelper:
    def __init__(self, driver):
        self.driver = driver

    def set_token(self, token):
        self.driver.execute_script(f"window.localStorage.setItem('token', '{token}');")

#Хелпер для работы с локальным хранилищем и Cookie
#Позволяет подставлять Auth-токен напрямую в LocalStorage браузера, пропуская шаги ввода логина/пароля на UI.