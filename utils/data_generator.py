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
    def generate_contact() -> Contact:
        return Contact(
            name=fake.first_name(),
            last_name=fake.last_name(),
            phone=fake.msisdn()[:10],  # 10-значный номер
            email=fake.email(),
            address=fake.address().replace("\n", ", "),
            description=fake.sentence()
        )