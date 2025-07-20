import pickle
from pathlib import Path
from contextlib import contextmanager
from books import AddressBook
from books import NoteBook


DATA_FILE = Path("data.pkl")


def save_data(address_book: AddressBook, note_book: NoteBook):
    """Serializes and saves the address book and note book to a file."""
    with open(DATA_FILE, "wb") as f:
        pickle.dump({"contacts": address_book, "notes": note_book}, f)


def load_data() -> tuple[AddressBook, NoteBook]:
    """Loads address book and note book or creates new ones"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "rb") as f:
            data = pickle.load(f)
            return data.get("contacts", AddressBook()), data.get("notes", NoteBook())
    return AddressBook(), NoteBook()


@contextmanager
def init_books_data():
    """Context manager for cli data (address book and note book)
    """

    # Access the address book and notebook from files, or create a new one if the files do not exist
    address_book, note_book = load_data()
    try:
        yield address_book, note_book
    finally:
        # Write the address book and notebook to files
        save_data(address_book, note_book)
