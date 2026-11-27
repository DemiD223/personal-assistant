
from assistant.notes.notebook import NoteBook
from assistant.notes.note import Note


def test_search_note():
    notebook = NoteBook()
    note_id = notebook.add(Note("Python project meeting"))

    results = notebook.find("python")

    assert note_id in results
    assert results[note_id].text == "Python project meeting"


def test_search_note_case_insensitive():
    notebook = NoteBook()
    notebook.add(Note("Python project meeting"))

    assert len(notebook.find("PYTHON")) == 1


def test_search_note_empty_query():
    notebook = NoteBook()
    notebook.add(Note("Python project meeting"))

    assert notebook.find("") == {}


def test_search_note_no_results():
    notebook = NoteBook()
    notebook.add(Note("Python project meeting"))

    assert notebook.find("Java") == {}
