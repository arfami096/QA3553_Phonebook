from dataclasses import dataclass

@dataclass
class Contact:
    name: str
    last_name: str
    phone: str
    email: str
    address: str
    description: str