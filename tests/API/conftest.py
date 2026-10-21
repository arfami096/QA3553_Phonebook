from types import SimpleNamespace

import pytest

from utils.api_data import build_contact, build_user
from utils.contact_api import ContactApi


@pytest.fixture(scope="session")
def api():
    """Один клиент на весь прогон: он не хранит состояния."""
    return ContactApi()


@pytest.fixture(scope="session")
def api_session_user(api):
    """Пользователь регистрируется ОДИН раз за прогон (scope="session"), а не перед каждым тестом.

    Так мы не плодим пользователей, а тесты быстрее. Удалить пользователя через API нельзя
    (в Swagger нет такого эндпоинта), поэтому лишние регистрации - это мусор, который останется навсегда.
    Контакты у каждого пользователя свои, поэтому изоляция тестов не страдает.
    """
    user = build_user()
    response = api.register(user)
    assert response.status_code == 200, f"Регистрация пользователя для тестов не удалась: {response.status_code} {response.text}"
    return SimpleNamespace(user=user, token=response.json()["token"])


@pytest.fixture
def token(api_session_user):
    return api_session_user.token


@pytest.fixture
def contacts_to_cleanup(api, token):
    """Для тестов, которые создают контакты сами. Добавьте email контакта в список,
    и после теста (даже упавшего) контакт будет удалён."""
    emails: list[str] = []
    yield emails
    for email in emails:
        contact = api.find_contact(email, token)
        if contact:
            api.delete_contact(contact["id"], token)


@pytest.fixture
def api_created_contact(api, token):
    """Контакт, созданный через API ДО теста и удалённый ПОСЛЕ него. Предусловие для тестов read/update/delete."""
    contact = build_contact()
    response = api.add_contact(contact, token)
    assert response.status_code == 200, f"Не удалось создать контакт: {response.status_code} {response.text}"

    saved = api.find_contact(contact.email, token)
    assert saved is not None, "Контакт создан, но не найден в списке"
    contact.id = saved["id"]

    yield contact

    # teardown: 404 допустим, если тест уже сам удалил контакт
    response = api.delete_contact(contact.id, token)
    if response.status_code not in (200, 404):
        print(f"Не удалось удалить контакт {contact.id}: {response.status_code} {response.text}")
