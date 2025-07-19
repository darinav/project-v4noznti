"""
Test module for note commands functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.note_commands import handle_note_command
from books import NoteBook, Note
from books.note_book.error import NoteNotFound


class TestNoteCommands:
    """Test cases for note commands functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.notebook = NoteBook()
        self.test_note = Note("Test Note", "This is a test note content", ["tag1", "tag2"])
        self.notebook.add_note(self.test_note)

    def test_handle_empty_command(self, capsys):
        """Test handling empty command."""
        handle_note_command("", self.notebook)
        captured = capsys.readouterr()
        assert "⚠️ Порожня команда." in captured.out

    def test_handle_whitespace_command(self, capsys):
        """Test handling whitespace-only command."""
        handle_note_command("   ", self.notebook)
        captured = capsys.readouterr()
        assert "⚠️ Порожня команда." in captured.out

    def test_add_note_basic(self, capsys):
        """Test adding a basic note."""
        handle_note_command('add note "New Note" "New content"', self.notebook)
        
        captured = capsys.readouterr()
        assert "✅ Нотатку 'New Note' додано." in captured.out

    def test_add_note_with_quotes(self, capsys):
        """Test adding note with quoted title and text."""
        handle_note_command('add note "Quoted Title" "Quoted content with spaces"', self.notebook)
        
        captured = capsys.readouterr()
        assert "✅ Нотатку 'Quoted Title' додано." in captured.out

    def test_add_note_without_quotes(self, capsys):
        """Test adding note without quotes."""
        handle_note_command('add note SimpleTitle Simple content', self.notebook)
        
        captured = capsys.readouterr()
        assert "✅ Нотатку 'SimpleTitle' додано." in captured.out

    def test_add_note_invalid(self, capsys):
        """Test adding note with invalid parameters."""
        handle_note_command('add note', self.notebook)
        
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out

    def test_add_note_exception(self, capsys):
        """Test adding note that causes exception."""
        # Create note with empty title to trigger exception
        handle_note_command('add note "" "Content"', self.notebook)
        
        captured = capsys.readouterr()
        assert "❌ Помилка:" in captured.out

    @patch('builtins.input')
    def test_edit_note_existing(self, mock_input, capsys):
        """Test editing an existing note."""
        mock_input.return_value = "Updated content"
        
        handle_note_command('edit note "Test Note"', self.notebook)
        
        captured = capsys.readouterr()
        assert "✅ Нотатку оновлено." in captured.out

    @patch('builtins.input')
    def test_edit_note_nonexistent(self, mock_input, capsys):
        """Test editing a note that doesn't exist."""
        mock_input.return_value = "New content"
        
        handle_note_command('edit note "Nonexistent Note"', self.notebook)
        
        captured = capsys.readouterr()
        assert "❌ Помилка:" in captured.out

    def test_edit_note_invalid_command(self, capsys):
        """Test edit note with invalid command format."""
        handle_note_command('edit note', self.notebook)
        
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out

    @patch('builtins.input')
    def test_edit_tag_existing(self, mock_input, capsys):
        """Test editing tags of an existing note."""
        mock_input.return_value = "newtag1 newtag2 newtag3"
        
        handle_note_command('edit tag "Test Note"', self.notebook)
        
        captured = capsys.readouterr()
        assert "✅ Теги оновлено." in captured.out

    @patch('builtins.input')
    def test_edit_tag_nonexistent(self, mock_input, capsys):
        """Test editing tags of a note that doesn't exist."""
        mock_input.return_value = "tag1 tag2"
        
        handle_note_command('edit tag "Nonexistent Note"', self.notebook)
        
        captured = capsys.readouterr()
        assert "❌ Помилка:" in captured.out

    def test_edit_tag_invalid_command(self, capsys):
        """Test edit tag with invalid command format."""
        handle_note_command('edit tag', self.notebook)
        
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out

    def test_delete_tag_existing(self, capsys):
        """Test deleting a tag from an existing note."""
        handle_note_command('delete tag "Test Note" tag1', self.notebook)
        
        captured = capsys.readouterr()
        assert "🗑️ Тег 'tag1' видалено." in captured.out

    def test_delete_tag_nonexistent_note(self, capsys):
        """Test deleting a tag from a note that doesn't exist."""
        handle_note_command('delete tag "Nonexistent Note" tag1', self.notebook)
        
        captured = capsys.readouterr()
        assert "❌ Помилка:" in captured.out

    def test_delete_tag_nonexistent_tag(self, capsys):
        """Test deleting a tag that doesn't exist from a note."""
        handle_note_command('delete tag "Test Note" nonexistent_tag', self.notebook)
        
        captured = capsys.readouterr()
        assert "❌ Помилка:" in captured.out

    def test_delete_tag_invalid_command(self, capsys):
        """Test delete tag with invalid command format."""
        handle_note_command('delete tag "Test Note"', self.notebook)
        
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out

    def test_delete_note_existing(self, capsys):
        """Test deleting an existing note."""
        handle_note_command('delete note "Test Note"', self.notebook)
        
        captured = capsys.readouterr()
        assert "🗑️ Нотатку 'Test Note' видалено." in captured.out

    def test_delete_note_nonexistent(self, capsys):
        """Test deleting a note that doesn't exist."""
        handle_note_command('delete note "Nonexistent Note"', self.notebook)
        
        captured = capsys.readouterr()
        assert "❌ Помилка:" in captured.out

    def test_delete_note_invalid_command(self, capsys):
        """Test delete note with invalid command format."""
        handle_note_command('delete note', self.notebook)
        
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out

    def test_search_note_found(self, capsys):
        """Test searching for a note that exists."""
        handle_note_command('search note test', self.notebook)
        
        captured = capsys.readouterr()
        assert "Test Note" in captured.out

    def test_search_note_not_found(self, capsys):
        """Test searching for a note that doesn't exist."""
        handle_note_command('search note nonexistent', self.notebook)
        
        captured = capsys.readouterr()
        # Should not crash, just show no results

    def test_search_note_by_content(self, capsys):
        """Test searching for a note by content."""
        handle_note_command('search note content', self.notebook)
        
        captured = capsys.readouterr()
        assert "Test Note" in captured.out

    def test_search_note_by_tag(self, capsys):
        """Test searching for a note by tag."""
        handle_note_command('search note tag1', self.notebook)
        
        captured = capsys.readouterr()
        assert "Test Note" in captured.out

    def test_search_note_invalid_command(self, capsys):
        """Test search note with invalid command format."""
        handle_note_command('search note', self.notebook)
        
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out

    def test_show_all_notes(self, capsys):
        """Test showing all notes."""
        handle_note_command('show all notes', self.notebook)
        
        captured = capsys.readouterr()
        assert "Test Note" in captured.out

    def test_show_all_notes_empty_notebook(self, capsys):
        """Test showing all notes when notebook is empty."""
        empty_notebook = NoteBook()
        handle_note_command('show all notes', empty_notebook)
        
        captured = capsys.readouterr()
        # Should not crash, just show nothing

    def test_sort_notes_by_tag(self, capsys):
        """Test sorting notes by tag."""
        # Add another note for sorting
        another_note = Note("Another Note", "Another content", ["ztag"])
        self.notebook.add_note(another_note)
        
        handle_note_command('sort notes by tag', self.notebook)
        
        captured = capsys.readouterr()
        # Should show notes sorted by tags

    def test_sort_notes_by_tag_empty_notebook(self, capsys):
        """Test sorting notes by tag when notebook is empty."""
        empty_notebook = NoteBook()
        handle_note_command('sort notes by tag', empty_notebook)
        
        captured = capsys.readouterr()
        # Should not crash, just show nothing

    def test_unknown_command(self, capsys):
        """Test handling unknown command."""
        handle_note_command('unknown command', self.notebook)
        
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out

    def test_add_note_with_hashtags(self, capsys):
        """Test adding note with hashtags in content."""
        handle_note_command('add note "Hashtag Note" "Content with #hashtag and #another"', self.notebook)
        
        captured = capsys.readouterr()
        assert "✅ Нотатку 'Hashtag Note' додано." in captured.out

    def test_edit_note_with_title_containing_spaces(self, capsys):
        """Test editing note with title containing spaces."""
        # Add a note with spaces in title
        spaced_note = Note("Note With Spaces", "Content")
        self.notebook.add_note(spaced_note)
        
        with patch('builtins.input') as mock_input:
            mock_input.return_value = "Updated content"
            handle_note_command('edit note "Note With Spaces"', self.notebook)
            
            captured = capsys.readouterr()
            assert "✅ Нотатку оновлено." in captured.out

    def test_delete_tag_with_spaces(self, capsys):
        """Test deleting tag that contains spaces or special characters."""
        # Add note with special tag
        special_note = Note("Special Note", "Content", ["tag with spaces"])
        self.notebook.add_note(special_note)
        
        handle_note_command('delete tag "Special Note" "tag with spaces"', self.notebook)
        
        captured = capsys.readouterr()
        # This might fail due to command parsing, but should be handled gracefully

    def test_search_note_multiple_words(self, capsys):
        """Test searching for notes with multiple word query."""
        handle_note_command('search note test content', self.notebook)
        
        captured = capsys.readouterr()
        # Should find the note that contains both words

    def test_add_note_empty_content(self, capsys):
        """Test adding note with empty content."""
        handle_note_command('add note "Empty Content" ""', self.notebook)
        
        captured = capsys.readouterr()
        assert "❌ Помилка:" in captured.out

    def test_add_note_empty_title(self, capsys):
        """Test adding note with empty title."""
        handle_note_command('add note "" "Some content"', self.notebook)
        
        captured = capsys.readouterr()
        assert "❌ Помилка:" in captured.out