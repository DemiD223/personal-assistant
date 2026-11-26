from collections import UserDict


class NoteBook(UserDict):
    """Store notes by unique ID."""
    def __init__(self):
        super().__init__()
        self._next_id = 1

    def add(self, note):
        """Add a note and return ID"""
        note_id = self._next_id
        self.data[note_id] = note
        self._next_id += 1
        return note_id

    def find(self, query):
        """Return notes by query"""
        query = query.lower()
        return {
            note_id: note
            for note_id, note in self.data.items()
            if query in note.text.lower()
        }

    def edit(self, note_id, new_text):
        """"Replace the text by ID"""
        if note_id not in self.data:
            raise KeyError(f"Note {note_id} not found")        
        self.data[note_id].text = new_text

    def delete(self, note_id):
        """Delete note by ID"""
        if note_id not in self.data:
            raise KeyError("Note {note_id} not found")
        del self.data[note_id]

