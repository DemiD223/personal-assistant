"""Field classes for contact records (from homework 06)."""

import re
from datetime import datetime


class Field:
    """Base class for all record fields."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Contact name, a required field."""


class Phone(Field):
    """Phone number that must contain exactly 10 digits."""

    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Email(Field):
    """Email with a basic format check."""

    def __init__(self, value):
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError("Invalid email format.")
        super().__init__(value)


class Address(Field):
    """Postal address as free text."""

    def __init__(self, value):
        if not value.strip():
            raise ValueError("Address cannot be empty.")
        super().__init__(value.strip())


class Birthday(Field):
    """Birthday in DD.MM.YYYY format."""

    def __init__(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        if date > datetime.now().date():
            raise ValueError("Birthday cannot be in the future.")
        super().__init__(date)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
