"""Record class: one contact with its fields (from homework 06)."""

from assistant.contacts.fields import Address, Birthday, Email, Name, Phone


class Record:
    """Contact with a name and a list of phones.

    Address, email and birthday fields are added by Developer 1.
    """

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.address = None
        self.birthday = None

    def add_phone(self, phone):
        """Add a new phone if it does not already exist."""
        if self.find_phone(phone):
            raise ValueError(f"Phone {phone} already exists.")

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

        if old_phone != new_phone and self.find_phone(new_phone):
            raise ValueError(f"Phone {new_phone} already exists.")

        new_phone_obj = Phone(new_phone)
        index = self.phones.index(phone_obj)
        self.phones[index] = new_phone_obj

    def add_email(self, email):
        """Set or replace the contact's email."""
        self.email = Email(email)

    def add_address(self, address):
        """Set or replace the contact's address."""
        self.address = Address(address)

    def add_birthday(self, birthday):
        """Set or replace the contact's birthday."""
        self.birthday = Birthday(birthday)

    def find_phone(self, phone):
        """Return the Phone object or None."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        parts = [f"Contact name: {self.name.value}", f"phones: {phones}"]
        if self.email:
            parts.append(f"email: {self.email}")
        if self.address:
            parts.append(f"address: {self.address}")
        if self.birthday:
            parts.append(f"birthday: {self.birthday}")
        return ", ".join(parts)
