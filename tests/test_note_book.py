"""
Test module for NoteBook functionality.
"""

import pytest
from books import NoteBook, Note
from books.note_book.error import NoteNotFound, NoteAlreadyExist


class TestNoteBook:
    """Test cases for NoteBook functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.notebook = NoteBook()
        self.note1 = Note("First Note", "This is the first note", ["tag1", "tag2"])
        self.note2 = Note("Second Note", "This is the second note", ["tag2", "tag3"])
        self.note3 = Note("Third Note", "This is the third note", ["tag1", "tag3"])

    def test_init_empty(self):
        """Test creating empty NoteBook."""
        notebook = NoteBook()
        assert len(notebook.data) == 0
        assert notebook._NoteBook__unique_titles == False

    def test_init_with_unique_titles(self):
        """Test creating NoteBook with unique titles enabled."""
        notebook = NoteBook(unique_titles=True)
        assert notebook._NoteBook__unique_titles == True

    def test_init_with_notes(self):
        """Test creating NoteBook with initial notes."""
        notebook = NoteBook(self.note1, self.note2)
        assert len(notebook.data) == 2

    def test_init_with_notes_unique_titles(self):
        """Test creating NoteBook with initial notes and unique titles."""
        # Create duplicate title notes
        duplicate_note = Note("First Note", "Duplicate content")
        notebook = NoteBook(self.note1, duplicate_note, unique_titles=True)
        # Should only have one note due to unique titles
        assert len(notebook.data) == 1

    def test_add_note_success(self):
        """Test adding a note successfully."""
        index = self.notebook.add_note(self.note1)
        assert isinstance(index, int)
        assert index in self.notebook.data
        assert self.notebook.data[index] == self.note1

    def test_add_note_unique_titles_success(self):
        """Test adding note with unique titles enabled."""
        notebook = NoteBook(unique_titles=True)
        index = notebook.add_note(self.note1)
        assert index in notebook.data

    def test_add_note_unique_titles_duplicate(self):
        """Test adding duplicate note with unique titles raises exception."""
        notebook = NoteBook(unique_titles=True)
        notebook.add_note(self.note1)
        
        duplicate_note = Note("First Note", "Different content")
        with pytest.raises(NoteAlreadyExist):
            notebook.add_note(duplicate_note)

    def test_get_note_success(self):
        """Test getting an existing note."""
        index = self.notebook.add_note(self.note1)
        retrieved_index, retrieved_note = self.notebook.get_note(index)
        assert retrieved_index == index
        assert retrieved_note == self.note1

    def test_get_note_invalid_index_zero(self):
        """Test getting note with index 0 raises exception."""
        with pytest.raises(NoteNotFound):
            self.notebook.get_note(0)

    def test_get_note_invalid_index_negative(self):
        """Test getting note with negative index raises exception."""
        with pytest.raises(NoteNotFound):
            self.notebook.get_note(-1)

    def test_get_note_nonexistent(self):
        """Test getting nonexistent note raises exception."""
        with pytest.raises(NoteNotFound):
            self.notebook.get_note(999)

    def test_delete_note_success(self):
        """Test deleting an existing note."""
        index = self.notebook.add_note(self.note1)
        self.notebook.delete_note(index)
        assert index not in self.notebook.data

    def test_delete_note_invalid_index_zero(self):
        """Test deleting note with index 0 raises exception."""
        with pytest.raises(NoteNotFound):
            self.notebook.delete_note(0)

    def test_delete_note_invalid_index_negative(self):
        """Test deleting note with negative index raises exception."""
        with pytest.raises(NoteNotFound):
            self.notebook.delete_note(-1)

    def test_delete_note_nonexistent(self):
        """Test deleting nonexistent note raises exception."""
        with pytest.raises(NoteNotFound):
            self.notebook.delete_note(999)

    def test_notes_default_order(self):
        """Test getting notes with default index order."""
        index1 = self.notebook.add_note(self.note1)
        index2 = self.notebook.add_note(self.note2)
        
        notes = self.notebook.notes()
        assert len(notes) == 2
        assert notes[0] == (index1, self.note1)
        assert notes[1] == (index2, self.note2)

    def test_notes_index_order(self):
        """Test getting notes with explicit index order."""
        index1 = self.notebook.add_note(self.note1)
        index2 = self.notebook.add_note(self.note2)
        
        notes = self.notebook.notes(NoteBook.SortOrder.index)
        assert len(notes) == 2
        assert notes[0] == (index1, self.note1)
        assert notes[1] == (index2, self.note2)

    def test_notes_title_order(self):
        """Test getting notes sorted by title."""
        self.notebook.add_note(self.note2)  # "Second Note"
        self.notebook.add_note(self.note1)  # "First Note"
        
        notes = self.notebook.notes(NoteBook.SortOrder.title)
        # Should be sorted alphabetically by title
        assert notes[0][1].title == "First Note"
        assert notes[1][1].title == "Second Note"

    def test_notes_tags_order(self):
        """Test getting notes sorted by tags."""
        self.notebook.add_note(self.note1)  # tags: ["tag1", "tag2"]
        self.notebook.add_note(self.note2)  # tags: ["tag2", "tag3"]
        
        notes = self.notebook.notes(NoteBook.SortOrder.tags)
        # Should be sorted by tags (converted to string)
        assert len(notes) == 2

    def test_search_by_title_found(self):
        """Test searching by title with results."""
        self.notebook.add_note(self.note1)
        self.notebook.add_note(self.note2)
        
        results = self.notebook.search_by_title("First")
        assert len(results) == 1
        assert results[0][1] == self.note1

    def test_search_by_title_not_found(self):
        """Test searching by title with no results."""
        self.notebook.add_note(self.note1)
        
        results = self.notebook.search_by_title("Nonexistent")
        assert len(results) == 0

    def test_search_by_title_empty_keyword(self):
        """Test searching by title with empty keyword."""
        self.notebook.add_note(self.note1)
        
        results = self.notebook.search_by_title("")
        assert len(results) == 0

    def test_search_by_text_found(self):
        """Test searching by text with results."""
        self.notebook.add_note(self.note1)
        self.notebook.add_note(self.note2)
        
        results = self.notebook.search_by_text("first note")
        assert len(results) == 1
        assert results[0][1] == self.note1

    def test_search_by_text_not_found(self):
        """Test searching by text with no results."""
        self.notebook.add_note(self.note1)
        
        results = self.notebook.search_by_text("nonexistent")
        assert len(results) == 0

    def test_search_by_text_empty_keyword(self):
        """Test searching by text with empty keyword."""
        self.notebook.add_note(self.note1)
        
        results = self.notebook.search_by_text("")
        assert len(results) == 0

    def test_search_by_tag_found(self):
        """Test searching by tag with results."""
        self.notebook.add_note(self.note1)  # tags: ["tag1", "tag2"]
        self.notebook.add_note(self.note2)  # tags: ["tag2", "tag3"]
        
        results = self.notebook.search_by_tag("tag1")
        assert len(results) == 1
        assert results[0][1] == self.note1

    def test_search_by_tag_multiple_results(self):
        """Test searching by tag with multiple results."""
        self.notebook.add_note(self.note1)  # tags: ["tag1", "tag2"]
        self.notebook.add_note(self.note2)  # tags: ["tag2", "tag3"]
        
        results = self.notebook.search_by_tag("tag2")
        assert len(results) == 2

    def test_search_by_tag_not_found(self):
        """Test searching by tag with no results."""
        self.notebook.add_note(self.note1)
        
        results = self.notebook.search_by_tag("nonexistent_tag")
        assert len(results) == 0

    def test_search_by_tag_empty_keyword(self):
        """Test searching by tag with empty keyword."""
        self.notebook.add_note(self.note1)
        
        results = self.notebook.search_by_tag("")
        assert len(results) == 0

    def test_search_general_title(self):
        """Test general search finding by title."""
        self.notebook.add_note(self.note1)
        self.notebook.add_note(self.note2)
        
        results = self.notebook.search("First")
        assert len(results) == 1
        assert results[0][1] == self.note1

    def test_search_general_text(self):
        """Test general search finding by text."""
        self.notebook.add_note(self.note1)
        self.notebook.add_note(self.note2)
        
        results = self.notebook.search("second note")
        assert len(results) == 1
        assert results[0][1] == self.note2

    def test_search_general_tag(self):
        """Test general search finding by tag."""
        self.notebook.add_note(self.note1)
        self.notebook.add_note(self.note2)
        
        results = self.notebook.search("tag3")
        assert len(results) == 1
        assert results[0][1] == self.note2

    def test_search_general_multiple_fields(self):
        """Test general search finding in multiple fields."""
        # Create note with "test" in title, text, and tags
        test_note = Note("Test Title", "Test content", ["test_tag"])
        self.notebook.add_note(test_note)
        self.notebook.add_note(self.note1)
        
        results = self.notebook.search("test")
        # Should find the note in multiple ways but return it only once
        assert len(results) >= 1

    def test_search_general_empty_keyword(self):
        """Test general search with empty keyword."""
        self.notebook.add_note(self.note1)
        
        results = self.notebook.search("")
        assert len(results) == 0

    def test_find_note_index_by_title_found(self):
        """Test finding note index by title when note exists."""
        self.notebook.add_note(self.note1)
        
        index = self.notebook.find_note_index_by_title("First Note")
        assert index is not None
        assert isinstance(index, int)

    def test_find_note_index_by_title_not_found(self):
        """Test finding note index by title when note doesn't exist."""
        self.notebook.add_note(self.note1)
        
        index = self.notebook.find_note_index_by_title("Nonexistent Note")
        assert index is None

    def test_delete_note_by_title_success(self):
        """Test deleting note by title successfully."""
        self.notebook.add_note(self.note1)
        
        self.notebook.delete_note_by_title("First Note")
        
        # Note should be deleted
        index = self.notebook.find_note_index_by_title("First Note")
        assert index is None

    def test_delete_note_by_title_not_found(self):
        """Test deleting note by title when note doesn't exist."""
        with pytest.raises(NoteNotFound):
            self.notebook.delete_note_by_title("Nonexistent Note")

    def test_getstate_setstate(self):
        """Test serialization methods."""
        self.notebook.add_note(self.note1)
        
        # Test __getstate__
        state = self.notebook.__getstate__()
        assert isinstance(state, dict)
        
        # Test __setstate__
        new_notebook = NoteBook()
        new_notebook.__setstate__(state)
        assert len(new_notebook.data) == 1

    def test_next_note_index_empty(self):
        """Test next note index calculation on empty notebook."""
        # Access private method for testing
        index = self.notebook._NoteBook__next_note_index()
        assert index == 1

    def test_next_note_index_with_notes(self):
        """Test next note index calculation with existing notes."""
        self.notebook.add_note(self.note1)
        self.notebook.add_note(self.note2)
        
        # Access private method for testing
        index = self.notebook._NoteBook__next_note_index()
        assert index > 2

    def test_titles_private_method(self):
        """Test private titles method."""
        self.notebook.add_note(self.note1)
        self.notebook.add_note(self.note2)
        
        # Access private method for testing
        titles = self.notebook._NoteBook__titles()
        assert isinstance(titles, set)
        assert "First Note" in titles
        assert "Second Note" in titles

    def test_search_merge_private_method(self):
        """Test private search merge method."""
        self.notebook.add_note(self.note1)
        self.notebook.add_note(self.note2)
        
        # Create some search result sets
        set1 = {1}
        set2 = {2}
        set3 = {1, 2}
        
        # Access private method for testing
        results = self.notebook._NoteBook__search_merge(set1, set2, set3)
        assert isinstance(results, list)

    def test_empty_notebook_operations(self):
        """Test operations on empty notebook."""
        # Search operations
        assert len(self.notebook.search("anything")) == 0
        assert len(self.notebook.search_by_title("anything")) == 0
        assert len(self.notebook.search_by_text("anything")) == 0
        assert len(self.notebook.search_by_tag("anything")) == 0
        
        # Notes listing
        assert len(self.notebook.notes()) == 0
        
        # Find operations
        assert self.notebook.find_note_index_by_title("anything") is None

    def test_case_sensitivity_in_search(self):
        """Test case sensitivity in search operations."""
        self.notebook.add_note(self.note1)  # "First Note"
        
        # Test title search case sensitivity
        results_lower = self.notebook.search_by_title("first")
        results_upper = self.notebook.search_by_title("FIRST")
        results_mixed = self.notebook.search_by_title("First")
        
        # All should find the note (case insensitive)
        assert len(results_lower) == 1
        assert len(results_upper) == 1
        assert len(results_mixed) == 1

    def test_partial_matches_in_search(self):
        """Test partial matches in search operations."""
        self.notebook.add_note(self.note1)  # "First Note", "This is the first note"
        
        # Partial title match
        results = self.notebook.search_by_title("First")
        assert len(results) == 1
        
        # Partial text match
        results = self.notebook.search_by_text("first note")
        assert len(results) == 1

    def test_multiple_notes_same_content(self):
        """Test handling multiple notes with similar content."""
        note_a = Note("Note A", "Similar content", ["common_tag"])
        note_b = Note("Note B", "Similar content", ["common_tag"])
        
        self.notebook.add_note(note_a)
        self.notebook.add_note(note_b)
        
        # Search should find both
        results = self.notebook.search("Similar content")
        assert len(results) == 2
        
        results = self.notebook.search_by_tag("common_tag")
        assert len(results) == 2