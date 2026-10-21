from dataclasses import replace

import pytest

from utils.api_data import build_user

pytestmark = pytest.mark.api


# ---------------------------- РЕГИСТРАЦИЯ ----------------------------
def test_registration_success(api):
    user = build_user()

    response = api.register(user)

    assert response.status_code == 200, f"получили {response.status_code}: {response.text}"
    token = response.json()["token"]
    assert isinstance(token, str) and token, "token должен быть непустой строкой"
    assert token.count(".") == 2, "Ожидаем JWT: три части, разделённые точками"


def test_registration_duplicate_user(api):
    user = build_user()
    first = api.register(user)
    assert first.status_code == 200, f"получили {first.status_code}: {first.text}"

    second = api.register(user)

    assert second.status_code == 409, f"получили {second.status_code}: {second.text}"


@pytest.mark.parametrize(
    "field, bad_value",
    [
        ("username", "not-an-email"),
        ("username", ""),
        ("password", ""),
        ("password", "123"),  # правила пароля в Swagger не описаны: если вернётся 200, это повод уточнить требования
    ],
    ids=["email without @", "empty email", "empty password", "short password"],
)
def test_registration_invalid_data(api, field, bad_value):
    user = build_user()
    payload = {"username": user.email, "password": user.password}
    payload[field] = bad_value

    response = api.register_raw(payload)

    assert response.status_code == 400, f"получили {response.status_code}: {response.text}"


@pytest.mark.parametrize("missing_field", ["username", "password"])
def test_registration_missing_field(api, missing_field):
    user = build_user()
    payload = {"username": user.email, "password": user.password}
    payload.pop(missing_field)

    response = api.register_raw(payload)

    assert response.status_code == 400, f"получили {response.status_code}: {response.text}"


# ------------------------------- ЛОГИН -------------------------------
def test_login_success(api, api_session_user):
    response = api.login(api_session_user.user)

    assert response.status_code == 200, f"получили {response.status_code}: {response.text}"
    token = response.json()["token"]
    assert isinstance(token, str) and token.count(".") == 2


def test_login_wrong_password(api, api_session_user):
    wrong = replace(api_session_user.user, password="WrongPassword999!")

    response = api.login(wrong)

    assert response.status_code == 401, f"получили {response.status_code}: {response.text}"


def test_login_unknown_user(api):
    response = api.login(build_user())  # такого пользователя никто не регистрировал

    assert response.status_code == 401, f"получили {response.status_code}: {response.text}"


def test_login_token_gives_access_to_contacts(api, api_session_user):
    """Токен из логина реально работает на защищённом эндпоинте."""
    token = api.login(api_session_user.user).json()["token"]

    response = api.get_contacts(token)

    assert response.status_code == 200, f"получили {response.status_code}: {response.text}"
