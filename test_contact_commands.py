"""
Test module for contact_commands.py functionality.

Tests the handle_contact_command function with all supported contact operations
including add, edit, delete, show, search, and birthday commands.
"""

import pytest
from unittest.mock import patch, MagicMock, call
from colorama import Fore

from contact_commands import handle_contact_command
from books import AddressBook, Record
from books.address_book.error import (
    ContactNotFound,
    ContactAlreadyExist,
    ContactPhoneAlreadyExist,
    ContactEmailAlreadyExist,
    ContactAddressAlreadyExist,
    ContactBirthdayAlreadyExist,
)


class TestHandleContactCommand:
    """Test cases for handle_contact_command function."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.book = MagicMock(spec=AddressBook)
        
    def test_empty_command(self, capsys):
        """Test handling of empty command."""
        handle_contact_command("", self.book)
        captured = capsys.readouterr()
        assert "⚠️ Порожня команда." in captured.out
        
    def test_whitespace_command(self, capsys):
        """Test handling of whitespace-only command."""
        handle_contact_command("   ", self.book)
        captured = capsys.readouterr()
        assert "⚠️ Порожня команда." in captured.out
    
    @patch('builtins.input')
    @patch('contact_commands.Record')
    def test_add_contact_success(self, mock_record_class, mock_input, capsys):
        """Test successful contact addition."""
        # Mock user inputs
        mock_input.side_effect = ["123456789", "test@email.com", "Test Address", "1990-01-01"]
        
        # Mock Record instance
        mock_record = MagicMock()
        mock_record_class.return_value = mock_record
        
        handle_contact_command("add contact John Doe", self.book)
        
        # Verify Record was created with correct name
        mock_record_class.assert_called_once_with("John Doe")
        
        # Verify methods were called on record
        mock_record.add_phone.assert_called_once_with("123456789")
        mock_record.add_email.assert_called_once_with("test@email.com")
        mock_record.add_address.assert_called_once_with("Test Address")
        mock_record.add_birthday.assert_called_once_with("1990-01-01")
        
        # Verify record was added to book
        self.book.add_record.assert_called_once_with(mock_record)
        
        # Verify success message
        captured = capsys.readouterr()
        assert "✅ Контакт 'John Doe' додано!" in captured.out
    
    @patch('builtins.input')
    @patch('contact_commands.Record')
    def test_add_contact_minimal_info(self, mock_record_class, mock_input, capsys):
        """Test contact addition with minimal information (only name)."""
        # Mock user inputs (all empty)
        mock_input.side_effect = ["", "", "", ""]
        
        # Mock Record instance
        mock_record = MagicMock()
        mock_record_class.return_value = mock_record
        
        handle_contact_command("add contact Jane Smith", self.book)
        
        # Verify Record was created with correct name
        mock_record_class.assert_called_once_with("Jane Smith")
        
        # Verify no additional methods were called (empty inputs)
        mock_record.add_phone.assert_not_called()
        mock_record.add_email.assert_not_called()
        mock_record.add_address.assert_not_called()
        mock_record.add_birthday.assert_not_called()
        
        # Verify record was added to book
        self.book.add_record.assert_called_once_with(mock_record)
        
        # Verify success message
        captured = capsys.readouterr()
        assert "✅ Контакт 'Jane Smith' додано!" in captured.out
    
    @patch('builtins.input')
    @patch('contact_commands.Record')
    def test_add_contact_exception(self, mock_record_class, mock_input, capsys):
        """Test contact addition with exception."""
        mock_input.side_effect = ["", "", "", ""]
        mock_record = MagicMock()
        mock_record_class.return_value = mock_record
        
        # Mock exception during add_record
        self.book.add_record.side_effect = Exception("Test error")
        
        handle_contact_command("add contact Test User", self.book)
        
        # Verify error message
        captured = capsys.readouterr()
        assert "❌ Помилка: Test error" in captured.out
    
    def test_add_contact_insufficient_args(self, capsys):
        """Test add contact command with insufficient arguments."""
        handle_contact_command("add", self.book)
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для контактів." in captured.out
        
        handle_contact_command("add contact", self.book)
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для контактів." in captured.out
    
    @patch('builtins.input')
    def test_edit_contact_success(self, mock_input, capsys):
        """Test successful contact editing."""
        # Mock user inputs
        mock_input.side_effect = ["987654321", "new@email.com", "New Address", "1985-05-05"]
        
        # Mock record
        mock_record = MagicMock()
        self.book.find.return_value = mock_record
        
        handle_contact_command("edit contact John Doe", self.book)
        
        # Verify record was found
        self.book.find.assert_called_once_with("John Doe")
        
        # Verify edit methods were called
        mock_record.edit_phone.assert_called_once_with(0, "987654321")
        mock_record.edit_email.assert_called_once_with(0, "new@email.com")
        mock_record.edit_address.assert_called_once_with(0, "New Address")
        mock_record.edit_birthday.assert_called_once_with("1985-05-05")
        
        # Verify success message
        captured = capsys.readouterr()
        assert "✅ Контакт 'John Doe' оновлено!" in captured.out
    
    @patch('builtins.input')
    def test_edit_contact_partial_update(self, mock_input, capsys):
        """Test contact editing with partial updates."""
        # Mock user inputs (some empty)
        mock_input.side_effect = ["987654321", "", "New Address", ""]
        
        # Mock record
        mock_record = MagicMock()
        self.book.find.return_value = mock_record
        
        handle_contact_command("edit contact John Doe", self.book)
        
        # Verify only non-empty fields were updated
        mock_record.edit_phone.assert_called_once_with(0, "987654321")
        mock_record.edit_email.assert_not_called()
        mock_record.edit_address.assert_called_once_with(0, "New Address")
        mock_record.edit_birthday.assert_not_called()
    
    @patch('builtins.input')
    def test_edit_contact_not_found(self, mock_input, capsys):
        """Test editing non-existent contact."""
        mock_input.side_effect = ["", "", "", ""]
        self.book.find.side_effect = Exception("Contact not found")
        
        handle_contact_command("edit contact NonExistent", self.book)
        
        # Verify error message
        captured = capsys.readouterr()
        assert "❌ Помилка: Contact not found" in captured.out
    
    def test_delete_contact_success(self, capsys):
        """Test successful contact deletion."""
        handle_contact_command("delete contact John Doe", self.book)
        
        # Verify delete was called
        self.book.delete_record.assert_called_once_with("John Doe")
        
        # Verify success message
        captured = capsys.readouterr()
        assert "🗑️ Контакт 'John Doe' видалено." in captured.out
    
    def test_delete_contact_not_found(self, capsys):
        """Test deleting non-existent contact."""
        self.book.delete_record.side_effect = Exception("Contact not found")
        
        handle_contact_command("delete contact NonExistent", self.book)
        
        # Verify error message
        captured = capsys.readouterr()
        assert "❌ Помилка: Contact not found" in captured.out
    
    def test_show_contact_success(self, capsys):
        """Test successful contact display."""
        mock_record = MagicMock()
        mock_record.__str__ = MagicMock(return_value="John Doe: 123456789")
        self.book.find.return_value = mock_record
        
        handle_contact_command("show contact John Doe", self.book)
        
        # Verify find was called
        self.book.find.assert_called_once_with("John Doe")
        
        # Verify record was printed
        captured = capsys.readouterr()
        assert "John Doe: 123456789" in captured.out
    
    def test_show_contact_not_found(self, capsys):
        """Test showing non-existent contact."""
        self.book.find.side_effect = Exception("Contact not found")
        
        handle_contact_command("show contact NonExistent", self.book)
        
        # Verify error message
        captured = capsys.readouterr()
        assert "❌ Помилка: Contact not found" in captured.out
    
    def test_show_all_contacts(self, capsys):
        """Test showing all contacts."""
        # Mock records
        mock_record1 = MagicMock()
        mock_record1.__str__ = MagicMock(return_value="John Doe: 123456789")
        mock_record2 = MagicMock()
        mock_record2.__str__ = MagicMock(return_value="Jane Smith: 987654321")
        
        self.book.__iter__ = MagicMock(return_value=iter([mock_record1, mock_record2]))
        
        handle_contact_command("show all contacts", self.book)
        
        # Verify all records were printed
        captured = capsys.readouterr()
        assert "John Doe: 123456789" in captured.out
        assert "Jane Smith: 987654321" in captured.out
    
    def test_show_birthdays_default_days(self, capsys):
        """Test showing birthdays with default days (7)."""
        # Mock records
        mock_record1 = MagicMock()
        mock_record1.__str__ = MagicMock(return_value="John Doe: Birthday in 3 days")
        mock_record2 = MagicMock()
        mock_record2.__str__ = MagicMock(return_value="Jane Smith: Birthday in 5 days")
        
        self.book.upcoming_birthdays_by_days.return_value = [mock_record1, mock_record2]
        
        handle_contact_command("show birthdays", self.book)
        
        # Verify method was called with default 7 days
        self.book.upcoming_birthdays_by_days.assert_called_once_with(7)
        
        # Verify records were printed
        captured = capsys.readouterr()
        assert "John Doe: Birthday in 3 days" in captured.out
        assert "Jane Smith: Birthday in 5 days" in captured.out
    
    def test_show_birthdays_custom_days(self, capsys):
        """Test showing birthdays with custom days."""
        mock_record = MagicMock()
        mock_record.__str__ = MagicMock(return_value="John Doe: Birthday in 2 days")
        
        self.book.upcoming_birthdays_by_days.return_value = [mock_record]
        
        handle_contact_command("show birthdays 3", self.book)
        
        # Verify method was called with custom 3 days
        self.book.upcoming_birthdays_by_days.assert_called_once_with(3)
        
        # Verify record was printed
        captured = capsys.readouterr()
        assert "John Doe: Birthday in 2 days" in captured.out
    
    def test_show_birthdays_exception(self, capsys):
        """Test showing birthdays with exception."""
        self.book.upcoming_birthdays_by_days.side_effect = Exception("Birthday error")
        
        handle_contact_command("show birthdays 5", self.book)
        
        # Verify error message
        captured = capsys.readouterr()
        assert "❌ Помилка: Birthday error" in captured.out
    
    def test_search_contact_success(self, capsys):
        """Test successful contact search."""
        # Mock search results
        mock_record1 = MagicMock()
        mock_record1.__str__ = MagicMock(return_value="John Doe: 123456789")
        mock_record2 = MagicMock()
        mock_record2.__str__ = MagicMock(return_value="John Smith: 987654321")
        
        self.book.search.return_value = [mock_record1, mock_record2]
        
        handle_contact_command("search contact John", self.book)
        
        # Verify search was called
        self.book.search.assert_called_once_with("John")
        
        # Verify results were printed
        captured = capsys.readouterr()
        assert "John Doe: 123456789" in captured.out
        assert "John Smith: 987654321" in captured.out
    
    def test_search_contact_multi_word(self, capsys):
        """Test contact search with multiple words."""
        mock_record = MagicMock()
        mock_record.__str__ = MagicMock(return_value="John Doe Smith: 123456789")
        
        self.book.search.return_value = [mock_record]
        
        handle_contact_command("search contact John Doe", self.book)
        
        # Verify search was called with full phrase
        self.book.search.assert_called_once_with("John Doe")
        
        # Verify result was printed
        captured = capsys.readouterr()
        assert "John Doe Smith: 123456789" in captured.out
    
    def test_search_contact_no_results(self, capsys):
        """Test contact search with no results."""
        self.book.search.return_value = []
        
        handle_contact_command("search contact NonExistent", self.book)
        
        # Verify search was called
        self.book.search.assert_called_once_with("NonExistent")
        
        # No output expected for empty results
        captured = capsys.readouterr()
        # Should not contain error messages
        assert "❌" not in captured.out
    
    def test_unknown_command(self, capsys):
        """Test handling of unknown command."""
        handle_contact_command("unknown command", self.book)
        
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для контактів." in captured.out
    
    def test_malformed_commands(self, capsys):
        """Test handling of malformed commands."""
        commands = [
            "add",
            "add something",
            "edit",
            "edit something",
            "delete",
            "delete something",
            "show",
            "show something",
            "search",
            "search something"
        ]
        
        for command in commands:
            handle_contact_command(command, self.book)
            captured = capsys.readouterr()
            assert "⚠️ Невідома команда для контактів." in captured.out
    
    def test_add_contact_with_spaces_in_name(self, capsys):
        """Test adding contact with spaces in name."""
        with patch('builtins.input') as mock_input, \
             patch('contact_commands.Record') as mock_record_class:
            
            mock_input.side_effect = ["", "", "", ""]
            mock_record = MagicMock()
            mock_record_class.return_value = mock_record
            
            handle_contact_command("add contact John Doe Smith Jr", self.book)
            
            # Verify Record was created with full name including spaces
            mock_record_class.assert_called_once_with("John Doe Smith Jr")
    
    def test_edit_contact_with_spaces_in_name(self, capsys):
        """Test editing contact with spaces in name."""
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["", "", "", ""]
            mock_record = MagicMock()
            self.book.find.return_value = mock_record
            
            handle_contact_command("edit contact John Doe Smith Jr", self.book)
            
            # Verify find was called with full name including spaces
            self.book.find.assert_called_once_with("John Doe Smith Jr")


if __name__ == "__main__":
    pytest.main([__file__])