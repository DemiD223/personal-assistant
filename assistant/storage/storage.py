import pickle
from pathlib import Path

DATA_DIR = Path.home() / ".personal_assistant"
CONTACTS_FILE = DATA_DIR / "addressbook.pkl"
NOTEBOOK_FILE = DATA_DIR / "notebook.pkl"


def save_data(data, path):
    """Save an object to a pickle file, creating the folder if needed."""
    DATA_DIR.mkdir(exist_ok=True)
    with open(path, "wb") as file:
        pickle.dump(data, file)


def load_data(path, default_factory):
    """Load an object from a pickle file or create a new one if missing."""
    if not path.exists():
        return default_factory()
    with open(path, "rb") as file:
        return pickle.load(file)
