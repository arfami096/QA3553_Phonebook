from dataclasses import dataclass


@dataclass
class Contact:
    name: str
    last_name: str
    phone: str
    email: str
    address: str
    description: str
    id: str | None = None  # id создаёт сервер, поэтому поле в конце и со значением по умолчанию

    def to_payload(self, with_id: bool = False) -> dict:
        """Словарь для json= в запросах. В API поле называется lastName, а не last_name."""
        payload = {
            "name": self.name,
            "lastName": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "description": self.description,
        }
        if with_id:
            payload["id"] = self.id
        return payload