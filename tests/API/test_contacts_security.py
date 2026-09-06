import allure
import requests


@allure.epic("Phonebook Application")
@allure.feature("API - Contact Management & Security")
class TestManagerContactsSecurity:

  @allure.story("Role: Manager")
  @allure.title("Manager successfully deletes contacts with a valid token")
  @allure.severity(allure.severity_level.CRITICAL)
  def test_manager_delete_all_success(self, valid_manager_headers):
    base_url = "https://contactapp-telran-backend.herokuapp.com"
    add_endpoint = f"{base_url}/v1/contacts"
    clear_endpoint = f"{base_url}/v1/contacts/clear"

    # Шаг 1. Предварительно создаем контакт, чтобы в базе точно было что удалять
    new_contact = {
        "name": "TestUser",
        "lastName": "Automation",
        "email": "test_automation@gmail.com",
        "phone": "1234567890",
        "address": "Berlin",
        "description": "Temporary contact for clear test",
    }

    with allure.step("Pre-condition: Add a new contact via API"):
      add_response = requests.post(
          add_endpoint, json=new_contact, headers=valid_manager_headers
      )
      # Проверяем, что контакт успешно создался (обычно 200 или 201)
      assert add_response.status_code in [
          200,
          201,
      ], f"Не удалось создать контакт перед тестом: {add_response.text}"

    with allure.step("Manager sends DELETE request to clear all contacts"):
      response = requests.delete(clear_endpoint, headers=valid_manager_headers)

    with allure.step("Verify contacts are successfully cleared"):
      assert response.status_code == 200, (
          f"Позитивный сценарий упал. Ожидался 200, пришел:"
          f" {response.status_code}"
      )

  @allure.story("Role: Manager")
  @allure.title(
      "F16: Delete all contacts with incorrect token_Contact returns error"
  )
  @allure.severity(allure.severity_level.CRITICAL)
  def test_manager_delete_all_with_invalid_token(self, invalid_manager_headers):
    base_url = "https://contactapp-telran-backend.herokuapp.com"
    endpoint = f"{base_url}/v1/contacts/clear"

    with allure.step(
        "Manager sends DELETE request using an invalid token (F16)"
    ):
      response = requests.delete(endpoint, headers=invalid_manager_headers)

    with allure.step(
        "Verify system blocks action and reports authorization error"
    ):
      # Фиксируем баг по ТЗ F16: ожидаем ошибку авторизации, но сервер может вернуть 404
      assert "Wrong authorization token!" in response.text or response.status_code in [
          401,
          400,
      ], (
          f"БАГ ПО F16: Сервер вернул код {response.status_code} и текст '{response.text}'"
          f" вместо ошибки авторизации 'Wrong authorization token!'."
      )