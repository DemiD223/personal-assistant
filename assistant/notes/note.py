from datetime import datetime


class Note:
    def __init__(self, text):
        self.text = text
        self.created_at = datetime.now()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not value or not value.strip():
            raise ValueError("Note text cannot be empty")
        self._text = value.strip()

    def __str__(self):
        date = self.created_at.strftime("%d.%m.%Y %H:%M")
        return f"{date} - {self.text}"
