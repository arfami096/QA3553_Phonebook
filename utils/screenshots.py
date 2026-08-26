import os
from datetime import datetime

def capture_failure(driver, test_name):
    os.makedirs("screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"screenshots/{test_name}_{timestamp}.png"
    driver.save_screenshot(file_path)
    return file_path

#Захват скриншотов и снятие DOM при падении
#Вспомогательная функция для сохранения скриншотов и исходного HTML-кода страницы в папку screenshots/ при падении теста.