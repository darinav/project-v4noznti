# -*- coding: utf-8 -*-

"""
Tests for NoteBook class
"""

import pytest
from books.note_book.book import NoteBook
from books.note_book.note import Note
from books.note_book.error.exceptions import NoteNotFound, NoteAlreadyExist


class TestNoteBook:
    """Tests for the NoteBook class"""

    @pytest.fixture
    def empty_book(self):
        """Return an empty note book"""
        return NoteBook()

    @pytest.fixture
    def sample_note(self, sample_title, sample_text, sample_tags):
        """Return a sample note"""
        return Note(sample_title, sample_text, sample_tags)

    @pytest.fixture
    def populated_book(self, sample_note):
        """Return a note book with a sample note"""
        book = NoteBook()
        book.add_note(sample_note)
        return book, 1  # Return the book and the index of the added note

    def test_initialization(self):
        """Test NoteBook initialization"""
        # Default initialization
        book = NoteBook()
        assert len(book) == 0
        assert book._NoteBook__unique_titles is False  # Default value

        # Custom unique_titles
        book = NoteBook(unique_titles=True)
        assert book._NoteBook__unique_titles is True

        # Initialize with notes
        note1 = Note("Title 1", "Text 1")
        note2 = Note("Title 2", "Text 2")
        book = NoteBook(note1, note2)
        assert len(book) == 2
        assert 1 in book  # First note should have index 1
        assert 2 in book  # Second note should have index 2

    def test_add_note(self, empty_book, sample_note):
        """Test adding a note"""
        # Add a note
        index = empty_book.add_note(sample_note)
        assert index == 1  # First note should have index 1
        assert index in empty_book
        assert empty_book[index] == sample_note

        # Add another note
        note2 = Note("Title 2", "Text 2")
        index2 = empty_book.add_note(note2)
        assert index2 == 2  # Second note should have index 2
        assert index2 in empty_book
        assert empty_book[index2] == note2

    def test_add_note_unique_titles(self, sample_title, sample_text):
        """Test adding a note with unique titles constraint"""
        book = NoteBook(unique_titles=True)
        
        # Add first note
        note1 = Note(sample_title, sample_text)
        index1 = book.add_note(note1)
        assert index1 == 1
        
        # Try to add another note with the same title
        note2 = Note(sample_title, "Different text")
        with pytest.raises(NoteAlreadyExist):
            book.add_note(note2)
        
        # Add note with different title
        note3 = Note("Different title", sample_text)
        index3 = book.add_note(note3)
        assert index3 == 2

    def test_get_note(self, populated_book):
        """Test getting a note"""
        book, index = populated_book
        
        # Get existing note
        retrieved_index, retrieved_note = book.get_note(index)
        assert retrieved_index == index
        assert retrieved_note == book[index]
        
        # Get non-existent note
        with pytest.raises(NoteNotFound):
            book.get_note(999)
        
        # Get note with invalid index
        with pytest.raises(NoteNotFound):
            book.get_note(0)
        with pytest.raises(NoteNotFound):
            book.get_note(-1)

    def test_delete_note(self, populated_book):
        """Test deleting a note"""
        book, index = populated_book
        
        # Delete existing note
        book.delete_note(index)
        assert index not in book
        
        # Delete non-existent note
        with pytest.raises(NoteNotFound):
            book.delete_note(index)
        
        # Delete note with invalid index
        with pytest.raises(NoteNotFound):
            book.delete_note(0)
        with pytest.raises(NoteNotFound):
            book.delete_note(-1)

    def test_notes_default_order(self, empty_book):
        """Test notes method with default order (index)"""
        # Add notes in reverse order to test sorting
        note3 = Note("Title 3", "Text 3")
        note2 = Note("Title 2", "Text 2")
        note1 = Note("Title 1", "Text 1")
        
        index3 = empty_book.add_note(note3)
        index2 = empty_book.add_note(note2)
        index1 = empty_book.add_note(note1)
        
        # Get notes with default order (index)
        notes = empty_book.notes()
        
        # Should be in order of addition
        assert len(notes) == 3
        assert notes[0][0] == index3
        assert notes[1][0] == index2
        assert notes[2][0] == index1

    def test_notes_title_order(self, empty_book):
        """Test notes method with title order"""
        # Add notes in reverse alphabetical order
        note_c = Note("Title C", "Text C")
        note_b = Note("Title B", "Text B")
        note_a = Note("Title A", "Text A")
        
        index_c = empty_book.add_note(note_c)
        index_b = empty_book.add_note(note_b)
        index_a = empty_book.add_note(note_a)
        
        # Get notes with title order
        notes = empty_book.notes(NoteBook.SortOrder.title)
        
        # Should be in alphabetical order by title
        assert len(notes) == 3
        assert notes[0][1].title == "Title A"
        assert notes[1][1].title == "Title B"
        assert notes[2][1].title == "Title C"

    def test_notes_tags_order(self, empty_book):
        """Test notes method with tags order"""
        # Add notes with different tags
        note_c = Note("Title 1", "Text 1", ["ztag"])
        note_b = Note("Title 2", "Text 2", ["mtag"])
        note_a = Note("Title 3", "Text 3", ["atag"])
        
        index_c = empty_book.add_note(note_c)
        index_b = empty_book.add_note(note_b)
        index_a = empty_book.add_note(note_a)
        
        # Get notes with tags order
        notes = empty_book.notes(NoteBook.SortOrder.tags)
        
        # Should be in alphabetical order by first tag
        assert len(notes) == 3
        assert "atag" in notes[0][1].tags
        assert "mtag" in notes[1][1].tags
        assert "ztag" in notes[2][1].tags

    def test_search_by_title(self, empty_book):
        """Test searching by title"""
        # Add notes with different titles
        note1 = Note("Project Plan", "Text 1")
        note2 = Note("Meeting Notes", "Text 2")
        note3 = Note("Shopping List", "Text 3")
        
        empty_book.add_note(note1)
        empty_book.add_note(note2)
        empty_book.add_note(note3)
        
        # Search for "Plan"
        results = empty_book.search_by_title("Plan")
        assert len(results) == 1
        assert results[0][1].title == "Project Plan"
        
        # Search for "Notes"
        results = empty_book.search_by_title("Notes")
        assert len(results) == 1
        assert results[0][1].title == "Meeting Notes"
        
        # Search for non-existent title
        results = empty_book.search_by_title("Non-existent")
        assert len(results) == 0
        
        # Search with empty keyword
        results = empty_book.search_by_title("")
        assert len(results) == 0

    def test_search_by_text(self, empty_book):
        """Test searching by text"""
        # Add notes with different text
        note1 = Note("Title 1", "This is about work projects")
        note2 = Note("Title 2", "Notes from the team meeting")
        note3 = Note("Title 3", "Grocery shopping list")
        
        empty_book.add_note(note1)
        empty_book.add_note(note2)
        empty_book.add_note(note3)
        
        # Search for "projects"
        results = empty_book.search_by_text("projects")
        assert len(results) == 1
        assert "projects" in results[0][1].text
        
        # Search for "meeting"
        results = empty_book.search_by_text("meeting")
        assert len(results) == 1
        assert "meeting" in results[0][1].text
        
        # Search for "shopping"
        results = empty_book.search_by_text("shopping")
        assert len(results) == 1
        assert "shopping" in results[0][1].text
        
        # Search for non-existent text
        results = empty_book.search_by_text("Non-existent")
        assert len(results) == 0
        
        # Search with empty keyword
        results = empty_book.search_by_text("")
        assert len(results) == 0

    def test_search_by_tag(self, empty_book):
        """Test searching by tag"""
        # Add notes with different tags
        note1 = Note("Title 1", "Text 1", ["work", "project"])
        note2 = Note("Title 2", "Text 2", ["meeting", "work"])
        note3 = Note("Title 3", "Text 3", ["personal", "shopping"])
        
        empty_book.add_note(note1)
        empty_book.add_note(note2)
        empty_book.add_note(note3)
        
        # Search for "work"
        results = empty_book.search_by_tag("work")
        assert len(results) == 2
        assert any("work" in result[1].tags for result in results)
        
        # Search for "project"
        results = empty_book.search_by_tag("project")
        assert len(results) == 1
        assert "project" in results[0][1].tags
        
        # Search for "personal"
        results = empty_book.search_by_tag("personal")
        assert len(results) == 1
        assert "personal" in results[0][1].tags
        
        # Search for non-existent tag
        results = empty_book.search_by_tag("Non-existent")
        assert len(results) == 0
        
        # Search with empty keyword
        results = empty_book.search_by_tag("")
        assert len(results) == 0

    def test_search(self, empty_book):
        """Test general search"""
        # Add notes with different attributes
        note1 = Note("Work Projects", "Planning for Q3 projects", ["work", "planning"])
        note2 = Note("Meeting Notes", "Notes from the team meeting", ["work", "meeting"])
        note3 = Note("Shopping List", "Grocery shopping list", ["personal", "shopping"])
        
        empty_book.add_note(note1)
        empty_book.add_note(note2)
        empty_book.add_note(note3)
        
        # Search for "work" (should find in title, text, and tags)
        results = empty_book.search("work")
        assert len(results) == 2
        assert any(result[1].title == "Work Projects" for result in results)
        assert any("work" in result[1].tags for result in results)
        
        # Search for "meeting" (should find in title, text, and tags)
        results = empty_book.search("meeting")
        assert len(results) == 1
        assert results[0][1].title == "Meeting Notes"
        assert "meeting" in results[0][1].text
        assert "meeting" in results[0][1].tags
        
        # Search for "shopping" (should find in title, text, and tags)
        results = empty_book.search("shopping")
        assert len(results) == 1
        assert results[0][1].title == "Shopping List"
        assert "shopping" in results[0][1].text
        assert "shopping" in results[0][1].tags
        
        # Search for "planning" (should find in text and tags)
        results = empty_book.search("planning")
        assert len(results) == 1
        assert "planning" in results[0][1].text.lower()
        assert "planning" in results[0][1].tags
        
        # Search for non-existent term
        results = empty_book.search("Non-existent")
        assert len(results) == 0
        
        # Search with empty keyword
        results = empty_book.search("")
        assert len(results) == 0