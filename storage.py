import pickle
from pathlib import Path
DATA_FILE = Path("data.pkl")

def save_data(address_book, note_book):
    """Serializes and saves the address book and note book to a file."""
    with open(DATA_FILE, "wb") as f:
        pickle.dump({"contacts": address_book, "notes": note_book}, f)

def load_data():
    """Loads address book and note book or creates new ones"""
if DATA_FILE.exists():
    with open(DATA_FILE, "rb") as f:
        data = pickle.load(f)
        return data.get("contacts"), data.get("notes")
    return AddressBook(), NoteBook()


