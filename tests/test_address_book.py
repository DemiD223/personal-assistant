
from assistant.contacts.address_book import AddressBook
from assistant.contacts.record import Record


def test_search_by_first_name():
    book = AddressBook()
    record = Record("Ivan Petrenko")
    record.add_phone("0671234567")
    book.add_record(record)

    results = book.search("ivan")

    assert len(results) == 1
    assert results[0].name.value == "Ivan Petrenko"


def test_search_by_last_name():
    book = AddressBook()
    record = Record("Ivan Petrenko")
    record.add_phone("0671234567")
    book.add_record(record)

    results = book.search("petrenko")

    assert len(results) == 1


def test_search_by_phone():
    book = AddressBook()
    record = Record("Ivan Petrenko")
    record.add_phone("0671234567")
    book.add_record(record)

    results = book.search("067")

    assert len(results) == 1


def test_search_empty_query():
    book = AddressBook()

    assert book.search("") == []


def test_search_no_results():
    book = AddressBook()
    record = Record("Ivan Petrenko")
    record.add_phone("0671234567")
    book.add_record(record)

    assert book.search("unknown") == []
