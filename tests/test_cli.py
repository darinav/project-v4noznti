"""
Test module for CLI functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli import print_main_menu, print_help, main


class TestCLI:
    """Test cases for CLI functionality."""

    def test_print_main_menu(self, capsys):
        """Test that main menu is printed correctly."""
        print_main_menu()
        captured = capsys.readouterr()
        assert "=== ГОЛОВНЕ МЕНЮ ===" in captured.out
        assert "1. Адресна книга" in captured.out
        assert "2. Нотатки" in captured.out
        assert "3. Допомога" in captured.out
        assert "0. Вихід" in captured.out

    def test_print_help(self, capsys):
        """Test that help is printed correctly."""
        print_help()
        captured = capsys.readouterr()
        assert "=== ДОСТУПНІ КОМАНДИ ===" in captured.out
        assert "[АДРЕСНА КНИГА]" in captured.out
        assert "[НОТАТКИ]" in captured.out
        assert "[ЗАГАЛЬНІ]" in captured.out
        assert "add contact" in captured.out
        assert "add note" in captured.out

    @patch('builtins.input')
    @patch('cli.cli.handle_contact_command')
    @patch('cli.cli.handle_note_command')
    def test_main_exit_immediately(self, mock_note_handler, mock_contact_handler, mock_input, capsys):
        """Test main function exits immediately when user chooses 0."""
        mock_input.return_value = "0"
        
        main()
        
        captured = capsys.readouterr()
        assert "👋 Вітаємо у Персональному помічнику!" in captured.out
        assert "👋 До побачення!" in captured.out
        mock_contact_handler.assert_not_called()
        mock_note_handler.assert_not_called()

    @patch('builtins.input')
    def test_main_help_option(self, mock_input, capsys):
        """Test main function shows help when user chooses 3."""
        mock_input.side_effect = ["3", "0"]
        
        main()
        
        captured = capsys.readouterr()
        assert "=== ДОСТУПНІ КОМАНДИ ===" in captured.out
        assert "👋 До побачення!" in captured.out

    @patch('builtins.input')
    def test_main_invalid_option(self, mock_input, capsys):
        """Test main function handles invalid menu option."""
        mock_input.side_effect = ["9", "0"]
        
        main()
        
        captured = capsys.readouterr()
        assert "⚠️ Невідома опція. Спробуйте ще раз." in captured.out
        assert "👋 До побачення!" in captured.out

    @patch('builtins.input')
    @patch('cli.cli.handle_contact_command')
    def test_main_contacts_mode(self, mock_contact_handler, mock_input, capsys):
        """Test main function enters contacts mode and handles commands."""
        mock_input.side_effect = ["1", "add contact John", "exit"]
        
        main()
        
        captured = capsys.readouterr()
        assert "👋 Вітаємо у Персональному помічнику!" in captured.out
        mock_contact_handler.assert_called_once()
        args = mock_contact_handler.call_args[0]
        assert args[0] == "add contact John"

    @patch('builtins.input')
    @patch('cli.cli.handle_note_command')
    def test_main_notes_mode(self, mock_note_handler, mock_input, capsys):
        """Test main function enters notes mode and handles commands."""
        mock_input.side_effect = ["2", "add note \"Test\" \"Content\"", "exit"]
        
        main()
        
        captured = capsys.readouterr()
        assert "👋 Вітаємо у Персональному помічнику!" in captured.out
        mock_note_handler.assert_called_once()
        args = mock_note_handler.call_args[0]
        assert args[0] == "add note \"Test\" \"Content\""

    @patch('builtins.input')
    @patch('cli.cli.handle_contact_command')
    @patch('cli.cli.handle_note_command')
    def test_main_switch_between_modes(self, mock_note_handler, mock_contact_handler, mock_input, capsys):
        """Test switching between contacts and notes modes."""
        mock_input.side_effect = ["1", "switch", "add note \"Test\" \"Content\"", "switch", "add contact John", "exit"]
        
        main()
        
        # Should have called both handlers
        mock_contact_handler.assert_called_once()
        mock_note_handler.assert_called_once()

    @patch('builtins.input')
    def test_main_help_in_contacts_mode(self, mock_input, capsys):
        """Test help command in contacts mode."""
        mock_input.side_effect = ["1", "help", "exit"]
        
        main()
        
        captured = capsys.readouterr()
        assert "=== ДОСТУПНІ КОМАНДИ ===" in captured.out

    @patch('builtins.input')
    def test_main_help_in_notes_mode(self, mock_input, capsys):
        """Test help command in notes mode."""
        mock_input.side_effect = ["2", "help", "exit"]
        
        main()
        
        captured = capsys.readouterr()
        assert "=== ДОСТУПНІ КОМАНДИ ===" in captured.out

    @patch('builtins.input')
    def test_main_close_command(self, mock_input, capsys):
        """Test close command works same as exit."""
        mock_input.side_effect = ["1", "close"]
        
        main()
        
        captured = capsys.readouterr()
        assert "👋 Вітаємо у Персональному помічнику!" in captured.out
        # Should exit without showing goodbye message since close is used in mode