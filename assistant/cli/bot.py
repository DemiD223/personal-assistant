"""Main command loop of the assistant (based on homework 05).

Handlers work with AddressBook and Record from homework 06.
"""

import shlex

from assistant.cli.decorators import input_error
from assistant.contacts import AddressBook, Record
from assistant.notes.note import Note
from assistant.notes.notebook import NoteBook
from assistant.storage.storage import (
    CONTACTS_FILE,
    NOTEBOOK_FILE,
    load_data,
    save_data,
)
from assistant.contacts.birthdays import get_upcoming_birthdays

MAIN_MENU = """Sections:
  contacts  - commands for contacts
  notes     - commands for notes
  help      - show this menu
  exit      - quit"""

SECTIONS = {
    "contacts": """Contacts:
  add <name> <phone>             - add a contact or a phone
  change <name> <old> <new>      - change a phone
  phone <name>                   - show phones of a contact
  all                            - show all contacts
  search-contact <query>         - search contacts
  add-email <name> <email>       - add an email
  add-address <name> <address>   - add an address
  add-birthday <name> <date>     - add a birthday (DD.MM.YYYY)
  show-birthday <name>           - show a birthday
  birthdays [N]                  - birthdays in the next N days""",
    "notes": """Notes:
  add-note <text>                - add a note
  edit-note <ID> <text>          - edit a note
  search-note <query>            - search notes
  delete-note <ID>               - delete a note""",
}


def parse_input(user_input: str):
    """Parse command and arguments with quoted strings.

    Examples:
        parse_input('add "John Doe" 12345')
        -> ('add', ['John Doe', '12345'])
        parse_input('change "John Doe" 12345 67890')
        -> ('change', ['John Doe', '12345', '67890'])
        parse_input('phone "John Doe"')
        -> ('phone', ['John Doe'])
        parse_input('add-note "Meeting at 10am"')
        -> ('add-note', ['Meeting at 10am'])
        parse_input('delete-note 1')
        -> ('delete-note', ['1'])
    """
    parts = shlex.split(user_input)

    if not parts:
        return "", []

    cmd, *args = parts
    return cmd.lower(), args


@input_error
def add_contact(args, book):
    """Add a new contact or a new phone to an existing one."""
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    """Replace an old phone of a contact with a new one."""
    if len(args) < 3:
        raise ValueError("Give me name, old phone and new phone please.")
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book):
    """Show all phones of a contact."""
    if not args:
        raise ValueError("Give me a name please.")
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    return "; ".join(p.value for p in record.phones) or "No phones."


@input_error
def add_email(args, book):
    """Add or replace a contact's email."""
    name, email = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    record.add_email(email)
    return "Email added."


@input_error
def add_address(args, book):
    """Add or replace a contact's address."""
    name, *address_parts = args
    if not address_parts:
        raise ValueError("Give me a name and an address please.")
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    record.add_address(" ".join(address_parts))
    return "Address added."


@input_error
def add_birthday(args, book):
    """Add or replace a contact's birthday (DD.MM.YYYY)."""
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    """Show a contact's birthday."""
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    if record.birthday is None:
        return f"{name} has no birthday set."
    return f"{name}: {record.birthday}"


@input_error
def birthdays(args, book):
    """Show birthdays in the next N days (7 by default)."""
    days = 7
    if args:
        if not args[0].isdigit():
            raise ValueError("Number of days must be a number.")
        days = int(args[0])

    upcoming = get_upcoming_birthdays(book, days)
    if not upcoming:
        return f"No birthdays in the next {days} days."

    return "\n".join(
        f"{record.name.value}: {when.strftime('%d.%m.%Y')}"
        for record, when in upcoming
    )


@input_error
def search_contact(args, book):
    """Search contacts by name or phone."""
    if not args:
        raise ValueError("Give me a search query please.")

    query = " ".join(args)
    results = book.search(query)

    if not results:
        return "No contacts found."

    return "\n".join(str(record) for record in results)


@input_error
def show_all(book):
    """Show all contacts."""
    if not book:
        return "No contacts saved."
    return "\n".join(str(record) for record in book.values())


@input_error
def add_note(args, notebook):
    """Add a new note."""
    if not args:
        raise ValueError("Give me note text please.")
    note = Note(" ".join(args))
    note_id = notebook.add(note)
    return f"Note {note_id} added."


@input_error
def search_note(args, notebook):
    """Search notes by text."""
    if not args:
        raise ValueError("Give me a search query please.")

    query = " ".join(args)
    results = notebook.find(query)

    if not results:
        return "No notes found."

    return "\n".join(
        f"ID: {note_id} | {note.text}"
        for note_id, note in results.items()
    )


@input_error
def edit_note(args, notebook):
    """Edit the text of a note by its ID."""
    if len(args) < 2:
        raise ValueError("Give me a note ID and new text please.")

    note_id, *text_parts = args
    if not note_id.isdigit():
        raise ValueError("Note ID must be a number.")

    notebook.edit(int(note_id), " ".join(text_parts))
    return f"Note {note_id} updated."


@input_error
def delete_note(args, notebook):
    """Delete a note by its ID."""
    if not args:
        raise ValueError("Give me note ID please.")
    if not args[0].isdigit():
        raise ValueError("Note ID must be a number.")
    note_id = int(args[0])
    notebook.delete(note_id)
    return f"Note {note_id} deleted."


def main():
    """Run the command loop until 'exit' or 'close'."""
    book = load_data(CONTACTS_FILE, AddressBook)
    notebook = load_data(NOTEBOOK_FILE, NoteBook)
    print("Welcome to the assistant bot!")
    print(MAIN_MENU)
    while True:
        try:
            user_input = input("Enter a command: ")
        except (KeyboardInterrupt, EOFError):
            print("\nGood bye!")
            break
        if not user_input.strip():
            print("Invalid command.")
            continue
        try:
            command, args = parse_input(user_input)
        except ValueError:
            print("Invalid command format. Check quotation marks.")
            continue

        if command in ("close", "exit"):
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "help":
            print(MAIN_MENU)
        elif command in SECTIONS:
            print(SECTIONS[command])
        elif command == "add":
            print(add_contact(args, book))
            save_data(book, CONTACTS_FILE)
        elif command == "change":
            print(change_contact(args, book))
            save_data(book, CONTACTS_FILE)
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "add-email":
            print(add_email(args, book))
            save_data(book, CONTACTS_FILE)
        elif command == "add-address":
            print(add_address(args, book))
            save_data(book, CONTACTS_FILE)
        elif command == "add-birthday":
            print(add_birthday(args, book))
            save_data(book, CONTACTS_FILE)
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "search-contact":
            print(search_contact(args, book))
        elif command == "add-note":
            print(add_note(args, notebook))
            save_data(notebook, NOTEBOOK_FILE)
        elif command == "search-note":
            print(search_note(args, notebook))
        elif command == "edit-note":
            print(edit_note(args, notebook))
            save_data(notebook, NOTEBOOK_FILE)
        elif command == "delete-note":
            print(delete_note(args, notebook))
            save_data(notebook, NOTEBOOK_FILE)
        else:
            print("Invalid command.")
