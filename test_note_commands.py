"""
Test module for note_commands.py functionality.

Tests the handle_note_command function with all supported note operations
including add, edit, delete, search, and tag management commands.
"""

import pytest
from unittest.mock import patch, MagicMock, call
from colorama import Fore

from note_commands import handle_note_command
from books import NoteBook, Note
from books.note_book.error import NoteNotFound, NoteAlreadyExist


class TestHandleNoteCommand:
    """Test cases for handle_note_command function."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.notebook = MagicMock(spec=NoteBook)
        
    def test_empty_command(self, capsys):
        """Test handling of empty command."""
        handle_note_command("", self.notebook)
        captured = capsys.readouterr()
        assert "⚠️ Порожня команда." in captured.out
        
    def test_whitespace_command(self, capsys):
        """Test handling of whitespace-only command."""
        handle_note_command("   ", self.notebook)
        captured = capsys.readouterr()
        assert "⚠️ Порожня команда." in captured.out
    
    @patch('note_commands.Note')
    def test_add_note_success(self, mock_note_class, capsys):
        """Test successful note addition."""
        # Mock Note instance
        mock_note = MagicMock()
        mock_note_class.return_value = mock_note
        
        handle_note_command('add note "Test Title" "Test content"', self.notebook)
        
        # Verify Note was created with correct title and text
        mock_note_class.assert_called_once_with("Test Title", "Test content")
        
        # Verify note was added to notebook
        self.notebook.add_note.assert_called_once_with(mock_note)
        
        # Verify success message
        captured = capsys.readouterr()
        assert "✅ Нотатку 'Test Title' додано." in captured.out
    
    @patch('note_commands.Note')
    def test_add_note_with_quotes(self, mock_note_class, capsys):
        """Test note addition with quoted title and text."""
        mock_note = MagicMock()
        mock_note_class.return_value = mock_note
        
        handle_note_command('add note "My Note" "This is my note content"', self.notebook)
        
        # Verify Note was created with correct title and text (quotes stripped)
        mock_note_class.assert_called_once_with("My Note", "This is my note content")
        
        # Verify note was added to notebook
        self.notebook.add_note.assert_called_once_with(mock_note)
    
    @patch('note_commands.Note')
    def test_add_note_multiword_content(self, mock_note_class, capsys):
        """Test note addition with multi-word content."""
        mock_note = MagicMock()
        mock_note_class.return_value = mock_note
        
        handle_note_command('add note "Title" "This is a long note with multiple words"', self.notebook)
        
        # Verify Note was created with full content
        mock_note_class.assert_called_once_with("Title", "This is a long note with multiple words")
    
    @patch('note_commands.Note')
    def test_add_note_exception(self, mock_note_class, capsys):
        """Test note addition with exception."""
        mock_note = MagicMock()
        mock_note_class.return_value = mock_note
        
        # Mock exception during add_note
        self.notebook.add_note.side_effect = Exception("Test error")
        
        handle_note_command('add note "Title" "Content"', self.notebook)
        
        # Verify error message
        captured = capsys.readouterr()
        assert "❌ Помилка: Test error" in captured.out
    
    def test_add_note_insufficient_args(self, capsys):
        """Test add note command with insufficient arguments."""
        handle_note_command("add", self.notebook)
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out
        
        handle_note_command("add note", self.notebook)
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out
    
    @patch('builtins.input')
    def test_edit_note_success(self, mock_input, capsys):
        """Test successful note editing."""
        # Mock user input
        mock_input.return_value = "New note content"
        
        # Mock note finding and retrieval
        self.notebook.find_note_index_by_title.return_value = 1
        mock_note = MagicMock()
        self.notebook.get_note.return_value = mock_note
        
        handle_note_command("edit note TestTitle", self.notebook)
        
        # Verify note was found
        self.notebook.find_note_index_by_title.assert_called_once_with("TestTitle")
        
        # Verify note was retrieved
        self.notebook.get_note.assert_called_once_with(1)
        
        # Verify note text was edited
        mock_note.edit_text.assert_called_once_with("New note content")
        
        # Verify success message
        captured = capsys.readouterr()
        assert "✅ Нотатку оновлено." in captured.out
    
    @patch('builtins.input')
    def test_edit_note_not_found(self, mock_input, capsys):
        """Test editing non-existent note."""
        mock_input.return_value = "New content"
        
        # Mock note not found
        self.notebook.find_note_index_by_title.return_value = None
        
        handle_note_command("edit note NonExistent", self.notebook)
        
        # Verify error message
        captured = capsys.readouterr()
        assert "❌ Помилка:" in captured.out
    
    @patch('builtins.input')
    def test_edit_note_exception(self, mock_input, capsys):
        """Test note editing with exception."""
        mock_input.return_value = "New content"
        
        # Mock exception during note finding
        self.notebook.find_note_index_by_title.side_effect = Exception("Test error")
        
        handle_note_command("edit note TestTitle", self.notebook)
        
        # Verify error message
        captured = capsys.readouterr()
        assert "❌ Помилка: Test error" in captured.out
    
    @patch('builtins.input')
    def test_edit_tag_success(self, mock_input, capsys):
        """Test successful tag editing."""
        # Mock user input
        mock_input.return_value = "tag1 tag2 tag3"
        
        # Mock note finding and retrieval
        self.notebook.find_note_index_by_title.return_value = 1
        mock_note = MagicMock()
        self.notebook.get_note.return_value = mock_note
        
        handle_note_command("edit tag TestTitle", self.notebook)
        
        # Verify note was found
        self.notebook.find_note_index_by_title.assert_called_once_with("TestTitle")
        
        # Verify note was retrieved
        self.notebook.get_note.assert_called_once_with(1)
        
        # Verify tags were replaced
        mock_note.replace_tags.assert_called_once_with(["tag1", "tag2", "tag3"])
        
        # Verify success message
        captured = capsys.readouterr()
        assert "✅ Теги оновлено." in captured.out
    
    @patch('builtins.input')
    def test_edit_tag_empty_input(self, mock_input, capsys):
        """Test tag editing with empty input."""
        # Mock empty user input
        mock_input.return_value = ""
        
        # Mock note finding and retrieval
        self.notebook.find_note_index_by_title.return_value = 1
        mock_note = MagicMock()
        self.notebook.get_note.return_value = mock_note
        
        handle_note_command("edit tag TestTitle", self.notebook)
        
        # Verify tags were replaced with empty list
        mock_note.replace_tags.assert_called_once_with([])
    
    @patch('builtins.input')
    def test_edit_tag_not_found(self, mock_input, capsys):
        """Test editing tags for non-existent note."""
        mock_input.return_value = "tag1 tag2"
        
        # Mock note not found
        self.notebook.find_note_index_by_title.return_value = None
        
        handle_note_command("edit tag NonExistent", self.notebook)
        
        # Verify error message
        captured = capsys.readouterr()
        assert "❌ Помилка:" in captured.out
    
    def test_delete_tag_success(self, capsys):
        """Test successful tag deletion."""
        # Mock note finding and retrieval
        self.notebook.find_note_index_by_title.return_value = 1
        mock_note = MagicMock()
        self.notebook.get_note.return_value = mock_note
        
        handle_note_command("delete tag TestTitle tagname", self.notebook)
        
        # Verify note was found
        self.notebook.find_note_index_by_title.assert_called_once_with("TestTitle")
        
        # Verify note was retrieved
        self.notebook.get_note.assert_called_once_with(1)
        
        # Verify tag was deleted
        mock_note.delete_tags.assert_called_once_with("tagname")
        
        # Verify success message
        captured = capsys.readouterr()
        assert "🗑️ Тег 'tagname' видалено." in captured.out
    
    def test_delete_tag_not_found(self, capsys):
        """Test deleting tag from non-existent note."""
        # Mock note not found
        self.notebook.find_note_index_by_title.return_value = None
        
        handle_note_command("delete tag NonExistent tagname", self.notebook)
        
        # Verify error message
        captured = capsys.readouterr()
        assert "❌ Помилка:" in captured.out
    
    def test_delete_tag_exception(self, capsys):
        """Test tag deletion with exception."""
        # Mock exception during note finding
        self.notebook.find_note_index_by_title.side_effect = Exception("Test error")
        
        handle_note_command("delete tag TestTitle tagname", self.notebook)
        
        # Verify error message
        captured = capsys.readouterr()
        assert "❌ Помилка: Test error" in captured.out
    
    def test_delete_note_success(self, capsys):
        """Test successful note deletion."""
        handle_note_command("delete note TestTitle", self.notebook)
        
        # Verify delete was called
        self.notebook.delete_note_by_title.assert_called_once_with("TestTitle")
        
        # Verify success message
        captured = capsys.readouterr()
        assert "🗑️ Нотатку 'TestTitle' видалено." in captured.out
    
    def test_delete_note_not_found(self, capsys):
        """Test deleting non-existent note."""
        self.notebook.delete_note_by_title.side_effect = Exception("Note not found")
        
        handle_note_command("delete note NonExistent", self.notebook)
        
        # Verify error message
        captured = capsys.readouterr()
        assert "❌ Помилка: Note not found" in captured.out
    
    def test_search_note_success(self, capsys):
        """Test successful note search."""
        # Mock search results
        mock_note1 = MagicMock()
        mock_note1.__str__ = MagicMock(return_value="Note 1: Test content")
        mock_note2 = MagicMock()
        mock_note2.__str__ = MagicMock(return_value="Note 2: Test content")
        
        self.notebook.search.return_value = [mock_note1, mock_note2]
        
        handle_note_command("search note test", self.notebook)
        
        # Verify search was called
        self.notebook.search.assert_called_once_with("test")
        
        # Verify results were printed
        captured = capsys.readouterr()
        assert "Note 1: Test content" in captured.out
        assert "Note 2: Test content" in captured.out
    
    def test_search_note_multi_word(self, capsys):
        """Test note search with multiple words."""
        mock_note = MagicMock()
        mock_note.__str__ = MagicMock(return_value="Found note")
        
        self.notebook.search.return_value = [mock_note]
        
        handle_note_command("search note test keyword", self.notebook)
        
        # Verify search was called with full phrase
        self.notebook.search.assert_called_once_with("test keyword")
        
        # Verify result was printed
        captured = capsys.readouterr()
        assert "Found note" in captured.out
    
    def test_search_note_no_results(self, capsys):
        """Test note search with no results."""
        self.notebook.search.return_value = []
        
        handle_note_command("search note nonexistent", self.notebook)
        
        # Verify search was called
        self.notebook.search.assert_called_once_with("nonexistent")
        
        # No output expected for empty results
        captured = capsys.readouterr()
        # Should not contain error messages
        assert "❌" not in captured.out
    
    def test_show_all_notes(self, capsys):
        """Test showing all notes."""
        # Mock notes
        mock_note1 = MagicMock()
        mock_note1.__str__ = MagicMock(return_value="Note 1: Content 1")
        mock_note2 = MagicMock()
        mock_note2.__str__ = MagicMock(return_value="Note 2: Content 2")
        
        self.notebook.notes.return_value = [mock_note1, mock_note2]
        
        handle_note_command("show all notes", self.notebook)
        
        # Verify notes method was called
        self.notebook.notes.assert_called_once()
        
        # Verify all notes were printed
        captured = capsys.readouterr()
        assert "Note 1: Content 1" in captured.out
        assert "Note 2: Content 2" in captured.out
    
    def test_sort_notes_by_tag(self, capsys):
        """Test sorting notes by tag."""
        # Mock notes
        mock_note1 = MagicMock()
        mock_note1.__str__ = MagicMock(return_value="Note A: #tag1")
        mock_note2 = MagicMock()
        mock_note2.__str__ = MagicMock(return_value="Note B: #tag2")
        
        self.notebook.notes.return_value = [mock_note1, mock_note2]
        
        handle_note_command("sort notes by tag", self.notebook)
        
        # Verify notes method was called with order="tags"
        self.notebook.notes.assert_called_once_with(order="tags")
        
        # Verify sorted notes were printed
        captured = capsys.readouterr()
        assert "Note A: #tag1" in captured.out
        assert "Note B: #tag2" in captured.out
    
    def test_unknown_command(self, capsys):
        """Test handling of unknown command."""
        handle_note_command("unknown command", self.notebook)
        
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out
    
    def test_malformed_commands(self, capsys):
        """Test handling of malformed commands."""
        commands = [
            "add",
            "add something",
            "edit",
            "edit something",
            "delete",
            "delete something",
            "search",
            "search something"
        ]
        
        for command in commands:
            handle_note_command(command, self.notebook)
            captured = capsys.readouterr()
            assert "⚠️ Невідома команда для нотаток." in captured.out
    
    def test_delete_tag_insufficient_args(self, capsys):
        """Test delete tag command with insufficient arguments."""
        handle_note_command("delete tag", self.notebook)
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out
        
        handle_note_command("delete tag title", self.notebook)
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out
    
    def test_delete_note_insufficient_args(self, capsys):
        """Test delete note command with insufficient arguments."""
        handle_note_command("delete note", self.notebook)
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out
    
    def test_search_note_insufficient_args(self, capsys):
        """Test search note command with insufficient arguments."""
        handle_note_command("search note", self.notebook)
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out
    
    def test_edit_note_insufficient_args(self, capsys):
        """Test edit note command with insufficient arguments."""
        handle_note_command("edit note", self.notebook)
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out
    
    def test_edit_tag_insufficient_args(self, capsys):
        """Test edit tag command with insufficient arguments."""
        handle_note_command("edit tag", self.notebook)
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для нотаток." in captured.out


if __name__ == "__main__":
    pytest.main([__file__])