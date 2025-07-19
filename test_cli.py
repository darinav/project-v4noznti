"""
Test module for cli.py functionality.

Tests the main CLI interface functions including menu display,
help display, and main application loop.
"""

import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock, call
from colorama import Fore

from cli import print_main_menu, print_help, main


class TestPrintMainMenu:
    """Test cases for print_main_menu function."""
    
    def test_print_main_menu_output(self, capsys):
        """Test that print_main_menu outputs the correct menu."""
        print_main_menu()
        captured = capsys.readouterr()
        
        # Check that the menu contains expected elements
        assert "=== ГОЛОВНЕ МЕНЮ ===" in captured.out
        assert "1. Адресна книга" in captured.out
        assert "2. Нотатки" in captured.out
        assert "3. Допомога" in captured.out
        assert "0. Вихід" in captured.out
        assert "switch" in captured.out
        assert "help" in captured.out
        assert "exit/close" in captured.out


class TestPrintHelp:
    """Test cases for print_help function."""
    
    def test_print_help_output(self, capsys):
        """Test that print_help outputs the correct help information."""
        print_help()
        captured = capsys.readouterr()
        
        # Check that help contains expected sections
        assert "=== ДОСТУПНІ КОМАНДИ ===" in captured.out
        assert "[АДРЕСНА КНИГА]" in captured.out
        assert "[НОТАТКИ]" in captured.out
        assert "[ЗАГАЛЬНІ]" in captured.out
        
        # Check contact commands
        assert "add contact <name>" in captured.out
        assert "edit contact <name>" in captured.out
        assert "show contact <name>" in captured.out
        assert "delete contact <name>" in captured.out
        assert "show all contacts" in captured.out
        assert "show birthdays <days>" in captured.out
        assert "search contact <keyword>" in captured.out
        
        # Check note commands
        assert "add note" in captured.out
        assert "edit note <title>" in captured.out
        assert "edit tag <title>" in captured.out
        assert "delete tag <title> <tag>" in captured.out
        assert "delete note <title>" in captured.out
        assert "search note <title>" in captured.out
        assert "show all notes" in captured.out
        assert "sort notes by tag" in captured.out


class TestMain:
    """Test cases for main function."""
    
    @patch('cli.AddressBook')
    @patch('cli.NoteBook')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_exit_immediately(self, mock_print, mock_input, mock_notebook, mock_addressbook):
        """Test main function exits immediately when user selects 0."""
        mock_input.return_value = "0"
        
        main()
        
        # Verify that AddressBook and NoteBook were initialized
        mock_addressbook.assert_called_once()
        mock_notebook.assert_called_once()
        
        # Verify welcome message was printed
        mock_print.assert_any_call(Fore.GREEN + "\n👋 Вітаємо у Персональному помічнику!")
        
        # Verify goodbye message was printed
        mock_print.assert_any_call(Fore.GREEN + "👋 До побачення!")
    
    @patch('cli.AddressBook')
    @patch('cli.NoteBook')
    @patch('cli.print_help')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_help_then_exit(self, mock_print, mock_input, mock_print_help, mock_notebook, mock_addressbook):
        """Test main function shows help then exits."""
        mock_input.side_effect = ["3", "0"]
        
        main()
        
        # Verify help was called
        mock_print_help.assert_called_once()
        
        # Verify goodbye message was printed
        mock_print.assert_any_call(Fore.GREEN + "👋 До побачення!")
    
    @patch('cli.AddressBook')
    @patch('cli.NoteBook')
    @patch('cli.print_help')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_help_command_then_exit(self, mock_print, mock_input, mock_print_help, mock_notebook, mock_addressbook):
        """Test main function shows help with 'help' command then exits."""
        mock_input.side_effect = ["help", "0"]
        
        main()
        
        # Verify help was called
        mock_print_help.assert_called_once()
    
    @patch('cli.AddressBook')
    @patch('cli.NoteBook')
    @patch('cli.handle_contact_command')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_contacts_mode_exit(self, mock_print, mock_input, mock_handle_contact, mock_notebook, mock_addressbook):
        """Test main function enters contacts mode and exits."""
        mock_input.side_effect = ["1", "exit"]
        
        main()
        
        # Verify contact command handler was not called (exit before any command)
        mock_handle_contact.assert_not_called()
    
    @patch('cli.AddressBook')
    @patch('cli.NoteBook')
    @patch('cli.handle_contact_command')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_contacts_mode_close(self, mock_print, mock_input, mock_handle_contact, mock_notebook, mock_addressbook):
        """Test main function enters contacts mode and closes."""
        mock_input.side_effect = ["1", "close"]
        
        main()
        
        # Verify contact command handler was not called (close before any command)
        mock_handle_contact.assert_not_called()
    
    @patch('cli.AddressBook')
    @patch('cli.NoteBook')
    @patch('cli.handle_contact_command')
    @patch('cli.print_help')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_contacts_mode_help_then_exit(self, mock_print, mock_input, mock_print_help, mock_handle_contact, mock_notebook, mock_addressbook):
        """Test main function enters contacts mode, shows help, then exits."""
        mock_input.side_effect = ["1", "help", "exit"]
        
        main()
        
        # Verify help was called
        mock_print_help.assert_called_once()
        
        # Verify contact command handler was not called
        mock_handle_contact.assert_not_called()
    
    @patch('cli.AddressBook')
    @patch('cli.NoteBook')
    @patch('cli.handle_contact_command')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_contacts_mode_switch_to_notes_then_exit(self, mock_print, mock_input, mock_handle_contact, mock_notebook, mock_addressbook):
        """Test main function switches from contacts to notes mode then exits."""
        mock_input.side_effect = ["1", "switch", "exit"]
        
        main()
        
        # Verify contact command handler was not called
        mock_handle_contact.assert_not_called()
    
    @patch('cli.AddressBook')
    @patch('cli.NoteBook')
    @patch('cli.handle_note_command')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_notes_mode_exit(self, mock_print, mock_input, mock_handle_note, mock_notebook, mock_addressbook):
        """Test main function enters notes mode and exits."""
        mock_input.side_effect = ["2", "exit"]
        
        main()
        
        # Verify note command handler was not called (exit before any command)
        mock_handle_note.assert_not_called()
    
    @patch('cli.AddressBook')
    @patch('cli.NoteBook')
    @patch('cli.handle_note_command')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_notes_mode_close(self, mock_print, mock_input, mock_handle_note, mock_notebook, mock_addressbook):
        """Test main function enters notes mode and closes."""
        mock_input.side_effect = ["2", "close"]
        
        main()
        
        # Verify note command handler was not called (close before any command)
        mock_handle_note.assert_not_called()
    
    @patch('cli.AddressBook')
    @patch('cli.NoteBook')
    @patch('cli.handle_note_command')
    @patch('cli.print_help')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_notes_mode_help_then_exit(self, mock_print, mock_input, mock_print_help, mock_handle_note, mock_notebook, mock_addressbook):
        """Test main function enters notes mode, shows help, then exits."""
        mock_input.side_effect = ["2", "help", "exit"]
        
        main()
        
        # Verify help was called
        mock_print_help.assert_called_once()
        
        # Verify note command handler was not called
        mock_handle_note.assert_not_called()
    
    @patch('cli.AddressBook')
    @patch('cli.NoteBook')
    @patch('cli.handle_note_command')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_notes_mode_switch_to_contacts_then_exit(self, mock_print, mock_input, mock_handle_note, mock_notebook, mock_addressbook):
        """Test main function switches from notes to contacts mode then exits."""
        mock_input.side_effect = ["2", "switch", "exit"]
        
        main()
        
        # Verify note command handler was not called
        mock_handle_note.assert_not_called()
    
    @patch('cli.AddressBook')
    @patch('cli.NoteBook')
    @patch('cli.handle_contact_command')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_contacts_mode_command_then_exit(self, mock_print, mock_input, mock_handle_contact, mock_notebook, mock_addressbook):
        """Test main function processes contact command then exits."""
        mock_addressbook_instance = mock_addressbook.return_value
        mock_input.side_effect = ["1", "show all contacts", "exit"]
        
        main()
        
        # Verify contact command handler was called with correct arguments
        mock_handle_contact.assert_called_once_with("show all contacts", mock_addressbook_instance)
    
    @patch('cli.AddressBook')
    @patch('cli.NoteBook')
    @patch('cli.handle_note_command')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_notes_mode_command_then_exit(self, mock_print, mock_input, mock_handle_note, mock_notebook, mock_addressbook):
        """Test main function processes note command then exits."""
        mock_notebook_instance = mock_notebook.return_value
        mock_input.side_effect = ["2", "show all notes", "exit"]
        
        main()
        
        # Verify note command handler was called with correct arguments
        mock_handle_note.assert_called_once_with("show all notes", mock_notebook_instance)
    
    @patch('cli.AddressBook')
    @patch('cli.NoteBook')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_invalid_option(self, mock_print, mock_input, mock_notebook, mock_addressbook):
        """Test main function handles invalid menu option."""
        mock_input.side_effect = ["5", "0"]
        
        main()
        
        # Verify error message was printed
        mock_print.assert_any_call(Fore.RED + "⚠️ Невідома опція. Спробуйте ще раз.")


if __name__ == "__main__":
    pytest.main([__file__])