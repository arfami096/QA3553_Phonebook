from dataclasses import replace

import allure
import pytest

from utils.api_asserts import assert_contact_matches
from utils.api_data import build_contact, random_phone

pytestmark = pytest.mark.api


@allure.title("Жизненный цикл контакта: создать -> прочитать -> изменить -> удалить")
def test_contact_full_lifecycle(api, token, contacts_to_cleanup):
    contact = build_contact()
    contacts_to_cleanup.append(contact.email)  # страховка: если тест упадёт посередине, контакт всё равно удалится

    with allure.step("Создать контакт"):
        response = api.add_contact(contact, token)
        assert response.status_code == 200, f"получили {response.status_code}: {response.text}"

    with allure.step("Прочитать: контакт есть в списке с теми же данными"):
        saved = api.find_contact(contact.email, token)
        assert saved is not None, "Контакт не появился в списке"
        assert_contact_matches(saved, contact)
        contact.id = saved["id"]

    with allure.step("Изменить телефон и описание"):
        updated = replace(contact, phone=random_phone(), description="updated description")
        response = api.update_contact(updated, token)
        assert response.status_code == 200, f"получили {response.status_code}: {response.text}"

    with allure.step("Проверить, что изменения сохранились, а остальные поля не пострадали"):
        saved = api.find_contact(contact.email, token)
        assert saved is not None
        assert saved["id"] == contact.id, "После обновления id изменился"
        assert_contact_matches(saved, updated)

    with allure.step("Удалить контакт"):
        response = api.delete_contact(contact.id, token)
        assert response.status_code == 200, f"получили {response.status_code}: {response.text}"

    with allure.step("Проверить, что контакта больше нет"):
        assert api.find_contact(contact.email, token) is None, "Контакт остался в списке после удаления"
