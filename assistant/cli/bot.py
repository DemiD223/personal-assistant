"""Main command loop of the assistant (based on homework 05).

Handlers work with AddressBook and Record from homework 06.
"""

from assistant.cli.decorators import input_error
from assistant.contacts import AddressBook, Record
from assistant.notes.note import Note
from assistant.notes.notebook import NoteBook

MENU = """Available commands:
  hello                          - greeting
  add <name> <phone>             - add a contact or a phone to it
  change <name> <old> <new>      - change a phone
  phone <name>                   - show phones of a contact
  all                            - show all contacts
  add-note <text>                - add a note
  delete-note <ID>               - delete a note
  help                           - show this menu
  exit | close                   - quit"""


def parse_input(user_input):
    """Split user input into a lowercase command and arguments."""
    cmd, *args = user_input.split()
    return cmd.strip().lower(), *args


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
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    return "; ".join(p.value for p in record.phones) or "No phones."


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
    book = AddressBook()
    notebook = NoteBook()
    print("Welcome to the assistant bot!")
    print(MENU)
    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            print("Invalid command.")
            continue
        command, *args = parse_input(user_input)

        if command in ("close", "exit"):
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "help":
            print(MENU)
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-note":
            print(add_note(args, notebook))
        elif command == "delete-note":
            print(delete_note(args, notebook))
        else:
            print("Invalid command.")
