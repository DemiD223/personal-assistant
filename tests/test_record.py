
import pytest

from assistant.contacts.record import Record


def test_add_phone():
    record = Record("Test User")

    record.add_phone("0671234567")

    assert len(record.phones) == 1
    assert record.phones[0].value == "0671234567"


def test_add_duplicate_phone():
    record = Record("Test User")
    record.add_phone("0671234567")

    with pytest.raises(ValueError, match="already exists"):
        record.add_phone("0671234567")

    assert len(record.phones) == 1


def test_edit_phone():
    record = Record("Test User")
    record.add_phone("0671234567")

    record.edit_phone("0671234567", "0677654321")

    assert record.phones[0].value == "0677654321"


def test_edit_phone_to_existing_number():
    record = Record("Test User")
    record.add_phone("0671234567")
    record.add_phone("0677654321")

    with pytest.raises(ValueError, match="already exists"):
        record.edit_phone("0677654321", "0671234567")

    assert len(record.phones) == 2


def test_edit_nonexistent_phone():
    record = Record("Test User")

    with pytest.raises(ValueError, match="Phone not found"):
        record.edit_phone("0000000000", "0671234567")
