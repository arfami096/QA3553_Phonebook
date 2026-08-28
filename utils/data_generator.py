from faker import Faker
from models.contact import Contact
from models.user import User

fake = Faker()


class DataGenerator:
    @staticmethod
    def generate_user() -> User:
        return User(
            email=fake.email(),
            password=f"P@{fake.password(length=10, special_chars=True)}1a"
        )

    @staticmethod
    def generate_contact(**overrides) -> Contact:

        data = {
            "name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.unique.numerify("05########"),
            "email": fake.unique.email(),
            "address": fake.address(),
            "description": fake.sentence()
        }

        data.update(overrides)

        return Contact(**data)
