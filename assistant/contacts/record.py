"""Record class: one contact with its fields (from homework 06)."""

from assistant.contacts.fields import Name, Phone


class Record:
    """Contact with a name and a list of phones.

    Address, email and birthday fields are added by Developer 1.
    """

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        """Add a new phone to the contact."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """Remove a phone if it exists."""
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        """Replace an old phone with a new one."""
        phone_obj = self.find_phone(old_phone)
        if not phone_obj:
            raise ValueError("Phone not found.")
        new_phone_obj = Phone(new_phone)
        index = self.phones.index(phone_obj)
        self.phones[index] = new_phone_obj

    def find_phone(self, phone):
        """Return the Phone object or None."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"
