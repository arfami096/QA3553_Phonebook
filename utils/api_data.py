import uuid

from faker import Faker

from models.contact import Contact
from models.user import User

fake = Faker()


def random_phone(length: int = 12) -> str:
    """Телефон из цифр. По Swagger допустимо от 10 до 15 цифр: ^\\d{10,15}$"""
    return fake.numerify("#" * length)


def build_contact(**overrides) -> Contact:
    """Валидный контакт с уникальным email. Любое поле можно подменить: build_contact(phone="abc")."""
    data = {
        "name": fake.first_name(),
        "last_name": fake.last_name(),
        "phone": random_phone(),
        "email": f"contact_{uuid.uuid4().hex[:10]}@example.com",
        "address": fake.city(),
        "description": fake.sentence(nb_words=4),
    }
    data.update(overrides)
    return Contact(**data)


def build_user(**overrides) -> User:
    """Новый пользователь с уникальным email. Пароль в формате, который уже принимал ваш API."""
    data = {
        "email": f"api_user_{uuid.uuid4().hex[:10]}@example.com",
        "password": "Password123!",
    }
    data.update(overrides)
    return User(**data)