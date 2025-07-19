"""
Test module for contact commands functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.contact_commands import handle_contact_command
from books import AddressBook, Record
from books.address_book.error import ContactNotFound


class TestContactCommands:
    """Test cases for contact commands functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.book = AddressBook()
        self.test_record = Record("John Doe")
        self.test_record.add_phone("+380123456789")
        self.test_record.add_email("john@example.com")
        self.test_record.add_address("123 Main St")
        self.test_record.add_birthday("15.01.1990")
        self.book.add_record(self.test_record)

    def test_handle_empty_command(self, capsys):
        """Test handling empty command."""
        handle_contact_command("", self.book)
        captured = capsys.readouterr()
        assert "⚠️ Порожня команда." in captured.out

    def test_handle_whitespace_command(self, capsys):
        """Test handling whitespace-only command."""
        handle_contact_command("   ", self.book)
        captured = capsys.readouterr()
        assert "⚠️ Порожня команда." in captured.out

    @patch('builtins.input')
    def test_add_contact_basic(self, mock_input, capsys):
        """Test adding a basic contact with name only."""
        mock_input.side_effect = ["", "", "", ""]  # Empty inputs for phone, email, address, birthday
        
        handle_contact_command("add contact Jane Smith", self.book)
        
        captured = capsys.readouterr()
        assert "✅ Контакт 'Jane Smith' додано!" in captured.out
        assert "Jane Smith" in self.book.data

    @patch('builtins.input')
    def test_add_contact_full(self, mock_input, capsys):
        """Test adding a contact with all fields."""
        mock_input.side_effect = ["+380987654321", "jane@example.com", "456 Oak Ave", "20.05.1985"]
        
        handle_contact_command("add contact Jane Smith", self.book)
        
        captured = capsys.readouterr()
        assert "✅ Контакт 'Jane Smith' додано!" in captured.out
        
        record = self.book.find("Jane Smith")
        assert len(record.phones) == 1
        assert len(record.emails) == 1
        assert record.address is not None
        assert record.birthday is not None

    @patch('builtins.input')
    def test_add_contact_invalid_phone(self, mock_input, capsys):
        """Test adding contact with invalid phone number."""
        mock_input.side_effect = ["invalid_phone", "", "", ""]
        
        handle_contact_command("add contact Invalid User", self.book)
        
        captured = capsys.readouterr()
        assert "❌ Помилка:" in captured.out

    @patch('builtins.input')
    def test_add_contact_invalid_email(self, mock_input, capsys):
        """Test adding contact with invalid email."""
        mock_input.side_effect = ["", "invalid_email", "", ""]
        
        handle_contact_command("add contact Invalid User", self.book)
        
        captured = capsys.readouterr()
        assert "❌ Помилка:" in captured.out

    @patch('builtins.input')
    def test_add_contact_invalid_birthday(self, mock_input, capsys):
        """Test adding contact with invalid birthday."""
        mock_input.side_effect = ["", "", "", "invalid_date"]
        
        handle_contact_command("add contact Invalid User", self.book)
        
        captured = capsys.readouterr()
        assert "❌ Помилка:" in captured.out

    @patch('builtins.input')
    def test_edit_contact_existing(self, mock_input, capsys):
        """Test editing an existing contact."""
        mock_input.side_effect = ["+380111222333", "newemail@example.com", "789 New St", "25.12.1990"]
        
        handle_contact_command("edit contact John Doe", self.book)
        
        captured = capsys.readouterr()
        assert "✅ Контакт 'John Doe' оновлено!" in captured.out

    @patch('builtins.input')
    def test_edit_contact_add_new_fields(self, mock_input, capsys):
        """Test editing contact that has no existing phone/email."""
        # Create contact without phone/email
        empty_record = Record("Empty User")
        self.book.add_record(empty_record)
        
        mock_input.side_effect = ["+380555666777", "new@example.com", "New Address", "01.01.2000"]
        
        handle_contact_command("edit contact Empty User", self.book)
        
        captured = capsys.readouterr()
        assert "✅ Контакт 'Empty User' оновлено!" in captured.out
        
        record = self.book.find("Empty User")
        assert len(record.phones) == 1
        assert len(record.emails) == 1

    @patch('builtins.input')
    def test_edit_contact_skip_fields(self, mock_input, capsys):
        """Test editing contact with empty inputs (skip fields)."""
        mock_input.side_effect = ["", "", "", ""]  # Skip all fields
        
        handle_contact_command("edit contact John Doe", self.book)
        
        captured = capsys.readouterr()
        assert "✅ Контакт 'John Doe' оновлено!" in captured.out

    def test_edit_nonexistent_contact(self, capsys):
        """Test editing a contact that doesn't exist."""
        handle_contact_command("edit contact Nonexistent User", self.book)
        
        captured = capsys.readouterr()
        assert "❌ Контакт 'Nonexistent User' не знайдено!" in captured.out

    def test_delete_existing_contact(self, capsys):
        """Test deleting an existing contact."""
        handle_contact_command("delete contact John Doe", self.book)
        
        captured = capsys.readouterr()
        assert "🗑️ Контакт 'John Doe' видалено." in captured.out
        
        with pytest.raises(ContactNotFound):
            self.book.find("John Doe")

    def test_delete_nonexistent_contact(self, capsys):
        """Test deleting a contact that doesn't exist."""
        handle_contact_command("delete contact Nonexistent User", self.book)
        
        captured = capsys.readouterr()
        assert "❌ Контакт 'Nonexistent User' не знайдено!" in captured.out

    def test_show_existing_contact(self, capsys):
        """Test showing an existing contact."""
        handle_contact_command("show contact John Doe", self.book)
        
        captured = capsys.readouterr()
        assert "John Doe" in captured.out

    def test_show_nonexistent_contact(self, capsys):
        """Test showing a contact that doesn't exist."""
        handle_contact_command("show contact Nonexistent User", self.book)
        
        captured = capsys.readouterr()
        assert "❌ Контакт 'Nonexistent User' не знайдено!" in captured.out

    def test_show_all_contacts(self, capsys):
        """Test showing all contacts."""
        handle_contact_command("show all contacts", self.book)
        
        captured = capsys.readouterr()
        assert "John Doe" in captured.out

    def test_show_all_contacts_empty_book(self, capsys):
        """Test showing all contacts when book is empty."""
        empty_book = AddressBook()
        handle_contact_command("show all contacts", empty_book)
        
        captured = capsys.readouterr()
        # Should not crash, just show nothing

    def test_show_birthdays_default(self, capsys):
        """Test showing birthdays with default 7 days."""
        handle_contact_command("show birthdays", self.book)
        
        captured = capsys.readouterr()
        # Should not crash

    def test_show_birthdays_custom_days(self, capsys):
        """Test showing birthdays with custom number of days."""
        handle_contact_command("show birthdays 30", self.book)
        
        captured = capsys.readouterr()
        # Should not crash

    def test_show_birthdays_invalid_days(self, capsys):
        """Test showing birthdays with invalid number of days."""
        handle_contact_command("show birthdays invalid", self.book)
        
        captured = capsys.readouterr()
        assert "❌ Помилка:" in captured.out

    def test_search_contact_found(self, capsys):
        """Test searching for a contact that exists."""
        handle_contact_command("search contact John", self.book)
        
        captured = capsys.readouterr()
        assert "John Doe" in captured.out

    def test_search_contact_not_found(self, capsys):
        """Test searching for a contact that doesn't exist."""
        handle_contact_command("search contact Nonexistent", self.book)
        
        captured = capsys.readouterr()
        # Should not show any results but not crash

    def test_search_contact_by_phone(self, capsys):
        """Test searching for a contact by phone number."""
        handle_contact_command("search contact 123456789", self.book)
        
        captured = capsys.readouterr()
        assert "John Doe" in captured.out

    def test_search_contact_by_email(self, capsys):
        """Test searching for a contact by email."""
        handle_contact_command("search contact john@example.com", self.book)
        
        captured = capsys.readouterr()
        assert "John Doe" in captured.out

    def test_unknown_command(self, capsys):
        """Test handling unknown command."""
        handle_contact_command("unknown command", self.book)
        
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для контактів." in captured.out

    @patch('builtins.input')
    def test_incomplete_add_command(self, mock_input, capsys):
        """Test incomplete add command now prompts for missing parameters."""
        mock_input.side_effect = ["John Smith", "", "", "", ""]
        
        handle_contact_command("add contact", self.book)
        
        captured = capsys.readouterr()
        assert "✅ Контакт 'John Smith' додано!" in captured.out

    def test_incomplete_edit_command(self, capsys):
        """Test incomplete edit command."""
        handle_contact_command("edit contact", self.book)
        
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для контактів." in captured.out

    def test_incomplete_delete_command(self, capsys):
        """Test incomplete delete command."""
        handle_contact_command("delete contact", self.book)
        
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для контактів." in captured.out

    def test_incomplete_show_command(self, capsys):
        """Test incomplete show command."""
        handle_contact_command("show contact", self.book)
        
        captured = capsys.readouterr()
        assert "⚠️ Невідома команда для контактів." in captured.out

    def test_add_contact_with_spaces_in_name(self, capsys):
        """Test adding contact with spaces in name."""
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["", "", "", ""]
            
            handle_contact_command("add contact John Michael Smith", self.book)
            
            captured = capsys.readouterr()
            assert "✅ Контакт 'John Michael Smith' додано!" in captured.out
            assert "John Michael Smith" in self.book.data