"""Field classes for contact records (from homework 06)."""


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
