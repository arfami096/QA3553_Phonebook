from models.contact import Contact


def assert_contact_matches(actual: dict, expected: Contact) -> None:
    """Сверяет контакт из ответа API с тем, что мы отправляли, по каждому полю.

    Сообщение об ошибке сразу показывает, какое именно поле не совпало.
    """
    for key, value in expected.to_payload().items():
        assert key in actual, f"В ответе нет поля {key}"
        assert actual[key] == value, f"Поле {key}: ожидали {value!r}, пришло {actual[key]!r}"
