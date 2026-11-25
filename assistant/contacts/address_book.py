"""AddressBook: storage of contact records (from homework 06)."""

from collections import UserDict


class AddressBook(UserDict):
    """Stores records by contact name."""

    def add_record(self, record):
        """Add or replace a record."""
        self.data[record.name.value] = record

    def find(self, name):
        """Return a record by name or None."""
        return self.data.get(name)

    def delete(self, name):
        """Delete a record by name if it exists."""
        if name in self.data:
            del self.data[name]
