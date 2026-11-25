"""Contacts package: fields, records and the address book."""

from assistant.contacts.address_book import AddressBook
from assistant.contacts.fields import Field, Name, Phone
from assistant.contacts.record import Record

__all__ = ["AddressBook", "Field", "Name", "Phone", "Record"]
