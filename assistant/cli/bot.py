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

MENU = """Available commands:
  hello                          - greeting
  add <name> <phone>             - add a contact or a phone to it
  change <name> <old> <new>      - change a phone
  phone <name>                   - show phones of a contact
  all                            - show all contacts
  search-contact <query>         - search contacts
  add-note <text>                - add a note
  search-note <query>            - search notes
  edit-note <ID> <text>          - edit a note
  delete-note <ID>               - delete a note
  help                           - show this menu
  exit | close                   - quit"""


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
    print(MENU)
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
            print(MENU)
        elif command == "add":
            print(add_contact(args, book))
            save_data(book, CONTACTS_FILE)
        elif command == "change":
            print(change_contact(args, book))
            save_data(book, CONTACTS_FILE)
        elif command == "phone":
            print(show_phone(args, book))
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
