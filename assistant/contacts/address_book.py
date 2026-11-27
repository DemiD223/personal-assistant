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

    def search(self, query: str):
        """
        Search contacts by partial name or phone number.
        """
        query = query.strip().lower()

        if not query:
            return []

        # It helps to search for phone numbers regardless of formatting
        phone_query = "".join(char for char in query if char.isdigit())

        results = []

        for record in self.data.values():
            name = record.name.value.lower()

            if query in name:
                results.append(record)
                continue

            for phone in record.phones:
                phone_number = "".join(
                    char for char in phone.value if char.isdigit()
                )

                if phone_query and phone_query in phone_number:
                    results.append(record)
                    break

        return results


"""
What we get after my implementation of the search method:
- search("ivan") — will find Ivan Petrenko;
- search("petrenko") — will find by last name;
- search("067") — will find by part of the phone number;
- search("") — will return an empty list.
"""
