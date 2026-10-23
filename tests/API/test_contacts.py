import uuid
from dataclasses import replace

import pytest

from utils.api_asserts import assert_contact_matches
from utils.api_data import build_contact, random_phone

pytestmark = pytest.mark.api

# Известное расхождение со Swagger: без токена API отвечает 403, а не 401.
# strict=True: когда баг починят и тест неожиданно пройдёт (XPASS), прогон упадёт и напомнит убрать xfail.
BUG_NO_TOKEN_403 = pytest.mark.xfail(
    reason="BUG: запрос без токена возвращает 403, по Swagger должно быть 401", strict=True
)
BAD_TOKENS = [
    pytest.param(None, id="no token", marks=BUG_NO_TOKEN_403),
    pytest.param("incorrect_token_999", id="invalid token"),
]

# Известное расхождение со Swagger: идентичный контакт создаётся повторно, а должен быть 409.
BUG_DUPLICATE_CONTACT = pytest.mark.xfail(
    reason="BUG: идентичный контакт создаётся повторно (200), по Swagger должно быть 409 Duplicate contact fields",
    strict=True,
)

# Известное расхождение со Swagger: несуществующий контакт даёт 400, а не 404.
BUG_NOT_FOUND_400 = pytest.mark.xfail(
    reason="BUG: несуществующий id возвращает 400, по Swagger должно быть 404", strict=True
)


# ------------------------------ СОЗДАНИЕ ------------------------------
def test_add_contact_success(api, token, contacts_to_cleanup):
    contact = build_contact()
    contacts_to_cleanup.append(contact.email)

    response = api.add_contact(contact, token)

    assert response.status_code == 200, f"получили {response.status_code}: {response.text}"  # по Swagger это 200, а не 201
    assert "message" in response.json()
    # POST не возвращает id, поэтому «контакт реально сохранился» проверяем через список
    saved = api.find_contact(contact.email, token)
    assert saved is not None, "Контакт не появился в списке после создания"
    assert_contact_matches(saved, contact)


@pytest.mark.parametrize("bad_token", BAD_TOKENS)
def test_add_contact_unauthorized(api, bad_token):
    response = api.add_contact(build_contact(), bad_token)

    assert response.status_code == 401, f"получили {response.status_code}: {response.text}"


@pytest.mark.parametrize("missing_field", ["name", "lastName", "address"])
def test_add_contact_missing_required_field(api, token, contacts_to_cleanup, missing_field):
    contact = build_contact()
    contacts_to_cleanup.append(contact.email)  # если API ошибочно создаст контакт, мы за ним уберём
    payload = contact.to_payload()
    payload.pop(missing_field)

    response = api.add_contact_raw(payload, token)

    assert response.status_code == 400, f"получили {response.status_code}: {response.text}"


@pytest.mark.parametrize(
    "bad_phone",
    ["", "abc", "123456789", "1" * 16, "+1234567890"],
    ids=["empty", "letters", "9 digits", "16 digits", "with plus"],
)
def test_add_contact_invalid_phone(api, token, contacts_to_cleanup, bad_phone):
    contact = build_contact(phone=bad_phone)
    contacts_to_cleanup.append(contact.email)

    response = api.add_contact(contact, token)

    assert response.status_code == 400, f"получили {response.status_code}: {response.text}"


@pytest.mark.parametrize("length", [10, 15], ids=["min 10 digits", "max 15 digits"])
def test_add_contact_phone_boundaries(api, token, contacts_to_cleanup, length):
    contact = build_contact(phone=random_phone(length))
    contacts_to_cleanup.append(contact.email)

    response = api.add_contact(contact, token)

    assert response.status_code == 200, f"получили {response.status_code}: {response.text}"


@BUG_DUPLICATE_CONTACT
def test_add_duplicate_contact(api, token, contacts_to_cleanup):
    contact = build_contact()
    contacts_to_cleanup.append(contact.email)
    first = api.add_contact(contact, token)
    assert first.status_code == 200, f"получили {first.status_code}: {first.text}"

    second = api.add_contact(contact, token)

    assert second.status_code == 409, f"получили {second.status_code}: {second.text}"


# ------------------------------- ЧТЕНИЕ -------------------------------
def test_get_contacts_contains_created_contact(api, token, api_created_contact):
    response = api.get_contacts(token)

    assert response.status_code == 200, f"получили {response.status_code}: {response.text}"
    contacts = response.json()["contacts"]
    assert isinstance(contacts, list)
    assert api_created_contact.id in [item["id"] for item in contacts]


def test_get_contacts_response_structure(api, token, api_created_contact):
    """Контракт: у созданного контакта в ответе есть все поля из Swagger."""
    saved = api.find_contact(api_created_contact.email, token)

    expected_keys = {"id", "name", "lastName", "email", "phone", "address", "description"}
    assert expected_keys <= set(saved), f"Не хватает полей: {expected_keys - set(saved)}"


@pytest.mark.parametrize("bad_token", BAD_TOKENS)
def test_get_contacts_unauthorized(api, bad_token):
    response = api.get_contacts(bad_token)

    assert response.status_code == 401, f"получили {response.status_code}: {response.text}"


# ------------------------------ ИЗМЕНЕНИЕ ------------------------------
def test_update_contact_success(api, token, api_created_contact):
    # PUT заменяет контакт целиком: шлём все поля, меняем только телефон
    updated = replace(api_created_contact, phone=random_phone())

    response = api.update_contact(updated, token)

    assert response.status_code == 200, f"получили {response.status_code}: {response.text}"
    saved = api.find_contact(updated.email, token)
    assert saved is not None
    assert_contact_matches(saved, updated)  # телефон новый, остальные поля прежние


@pytest.mark.parametrize("missing_field", ["name", "lastName", "address"])
def test_update_contact_missing_required_field(api, token, api_created_contact, missing_field):
    payload = api_created_contact.to_payload(with_id=True)
    payload.pop(missing_field)

    response = api.update_contact_raw(payload, token)

    assert response.status_code == 400, f"получили {response.status_code}: {response.text}"


def test_update_contact_invalid_phone(api, token, api_created_contact):
    updated = replace(api_created_contact, phone="abc")

    response = api.update_contact(updated, token)

    assert response.status_code == 400, f"получили {response.status_code}: {response.text}"


@BUG_NOT_FOUND_400
def test_update_contact_not_found(api, token, api_created_contact):
    missing = replace(api_created_contact, id=str(uuid.uuid4()))

    response = api.update_contact(missing, token)

    assert response.status_code == 404, f"получили {response.status_code}: {response.text}"


@pytest.mark.parametrize("bad_token", BAD_TOKENS)
def test_update_contact_unauthorized(api, api_created_contact, bad_token):
    response = api.update_contact(api_created_contact, bad_token)

    assert response.status_code == 401, f"получили {response.status_code}: {response.text}"


# ------------------------------- УДАЛЕНИЕ -------------------------------
def test_delete_contact_success(api, token, api_created_contact):
    response = api.delete_contact(api_created_contact.id, token)

    assert response.status_code == 200, f"получили {response.status_code}: {response.text}"
    assert api.find_contact(api_created_contact.email, token) is None, "Контакт остался в списке после удаления"


@BUG_NOT_FOUND_400
def test_delete_contact_not_found(api, token):
    response = api.delete_contact(str(uuid.uuid4()), token)

    assert response.status_code == 404, f"получили {response.status_code}: {response.text}"


@pytest.mark.parametrize("bad_token", BAD_TOKENS)
def test_delete_contact_unauthorized(api, api_created_contact, bad_token):
    response = api.delete_contact(api_created_contact.id, bad_token)

    assert response.status_code == 401, f"получили {response.status_code}: {response.text}"
