from datetime import datetime


class Note:
    def __init__(self, text):
        if not text or not text.strip():
            raise ValueError("Note text can not be empty!")
        self.text = text.strip()
        self.created_at = datetime.now()

    def __str__(self):
        date = self.created_at.strftime("%d.%m.%Y %H:%M")
        return f"{date} - {self.text}"
