import unittest
from books.note_book.book import NoteBook
from books.note_book.note.note import Note
from books.note_book.error.exceptions import NoteNotFound, NoteAlreadyExist


class TestNoteBook(unittest.TestCase):
    def setUp(self):
        # Create test notes
        self.note1 = Note(
            title="Meeting Notes",
            text="Discuss project timeline #work #meeting",
            tags=["important"]
        )
        self.note2 = Note(
            title="Shopping List",
            text="Buy groceries and household items #personal",
            tags=["todo"]
        )
        self.note3 = Note(
            title="Project Ideas",
            text="New ideas for the upcoming project #work #brainstorm",
            tags=["creative"]
        )
        
        # Create notebook with notes
        self.notebook = NoteBook(self.note1, self.note2)

    def test_init(self):
        # Test initialization with notes
        self.assertEqual(len(self.notebook), 2)
        self.assertIn("Meeting Notes", self.notebook)
        self.assertIn("Shopping List", self.notebook)
        
        # Test initialization with duplicate notes (should only add unique ones)
        notebook = NoteBook(self.note1, self.note1, self.note2)
        self.assertEqual(len(notebook), 2)
        
        # Test initialization with no notes
        empty_notebook = NoteBook()
        self.assertEqual(len(empty_notebook), 0)

    def test_notes(self):
        # Test default sorting (by title)
        notes = self.notebook.notes()
        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0].title, "Meeting Notes")  # Alphabetically first
        self.assertEqual(notes[1].title, "Shopping List")  # Alphabetically second
        
        # Add a note with a title that comes before the others alphabetically
        self.notebook.add_note(self.note3)
        notes = self.notebook.notes()
        self.assertEqual(len(notes), 3)
        self.assertEqual(notes[0].title, "Meeting Notes")
        self.assertEqual(notes[1].title, "Project Ideas")
        self.assertEqual(notes[2].title, "Shopping List")
        
        # Test sorting by tags
        notes = self.notebook.notes(order=NoteBook.SortOrder.tags)
        self.assertEqual(len(notes), 3)
        # Should be sorted by the first tag alphabetically
        # creative, important, todo
        self.assertEqual(notes[0].title, "Project Ideas")  # Has tag "creative"
        self.assertEqual(notes[1].title, "Meeting Notes")  # Has tag "important"
        self.assertEqual(notes[2].title, "Shopping List")  # Has tag "todo"

    def test_find(self):
        # Test finding existing note
        note = self.notebook.find("Meeting Notes")
        self.assertEqual(note.title, "Meeting Notes")
        
        # Test finding non-existent note
        with self.assertRaises(NoteNotFound):
            self.notebook.find("Nonexistent Note")

    def test_add_note(self):
        # Test adding new note
        self.notebook.add_note(self.note3)
        self.assertEqual(len(self.notebook), 3)
        self.assertIn("Project Ideas", self.notebook)
        
        # Test adding duplicate note
        with self.assertRaises(NoteAlreadyExist):
            self.notebook.add_note(self.note1)

    def test_delete_note(self):
        # Test deleting existing note
        self.notebook.delete_note("Meeting Notes")
        self.assertEqual(len(self.notebook), 1)
        self.assertNotIn("Meeting Notes", self.notebook)
        
        # Test deleting non-existent note
        with self.assertRaises(NoteNotFound):
            self.notebook.delete_note("Nonexistent Note")


if __name__ == "__main__":
    unittest.main()