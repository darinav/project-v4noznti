import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.guess_command.guess_command import (
    _suggest_command,
    _is_general_command,
    _find_best_match,
    handle_command_with_guess
)
from cli.guess_command.possible_commands import GENERAL_COMMANDS


class TestSuggestCommand(unittest.TestCase):
    """Test cases for _suggest_command function"""
    
    def test_suggest_command_exact_match(self):
        """Test when user input exactly matches a valid command"""
        valid_commands = ["add contact", "edit contact", "show contact"]
        result = _suggest_command("add contact", valid_commands)
        self.assertEqual(result, "add contact")
    
    def test_suggest_command_close_match(self):
        """Test when user input is close to a valid command"""
        valid_commands = ["add contact", "edit contact", "show contact"]
        result = _suggest_command("ad contact", valid_commands, cutoff=0.5)
        self.assertEqual(result, "add contact")
    
    def test_suggest_command_no_match(self):
        """Test when user input doesn't match any valid command"""
        valid_commands = ["add contact", "edit contact", "show contact"]
        result = _suggest_command("xyz", valid_commands)
        self.assertIsNone(result)
    
    def test_suggest_command_empty_input(self):
        """Test with empty user input"""
        valid_commands = ["add contact", "edit contact"]
        result = _suggest_command("", valid_commands)
        self.assertIsNone(result)
    
    def test_suggest_command_empty_commands(self):
        """Test with empty valid commands list"""
        result = _suggest_command("add contact", [])
        self.assertIsNone(result)
    
    def test_suggest_command_none_input(self):
        """Test with None as user input"""
        valid_commands = ["add contact", "edit contact"]
        result = _suggest_command(None, valid_commands)
        self.assertIsNone(result)
    
    def test_suggest_command_custom_cutoff(self):
        """Test with custom cutoff value"""
        valid_commands = ["add contact", "edit contact"]
        # With high cutoff, should not match
        result = _suggest_command("ad", valid_commands, cutoff=0.9)
        self.assertIsNone(result)
        
        # With low cutoff, should match
        result = _suggest_command("ad", valid_commands, cutoff=0.1)
        self.assertEqual(result, "add contact")


class TestIsGeneralCommand(unittest.TestCase):
    """Test cases for _is_general_command function"""
    
    def test_is_general_command_true(self):
        """Test with commands that are in GENERAL_COMMANDS"""
        for cmd in GENERAL_COMMANDS:
            with self.subTest(cmd=cmd):
                self.assertTrue(_is_general_command(cmd))
    
    def test_is_general_command_case_insensitive(self):
        """Test that function is case insensitive"""
        self.assertTrue(_is_general_command("EXIT"))
        self.assertTrue(_is_general_command("Help"))
        self.assertTrue(_is_general_command("SWITCH"))
    
    def test_is_general_command_false(self):
        """Test with commands that are not in GENERAL_COMMANDS"""
        self.assertFalse(_is_general_command("add contact"))
        self.assertFalse(_is_general_command("edit note"))
        self.assertFalse(_is_general_command("unknown"))
    
    def test_is_general_command_empty_string(self):
        """Test with empty string"""
        self.assertFalse(_is_general_command(""))


class TestFindBestMatch(unittest.TestCase):
    """Test cases for _find_best_match function"""
    
    def setUp(self):
        self.valid_commands = [
            "add contact",
            "edit contact", 
            "show contact",
            "delete contact",
            "show all contacts",
            "add note",
            "edit note"
        ]
    
    def test_find_best_match_exact_match(self):
        """Test when command exactly matches"""
        result = _find_best_match("add contact", self.valid_commands)
        self.assertEqual(result, "add contact")
    
    def test_find_best_match_prefix_match(self):
        """Test when command is a prefix of a valid command"""
        result = _find_best_match("add", self.valid_commands)
        # Should return one of the commands starting with "add"
        self.assertIn(result, ["add contact", "add note"])
    
    def test_find_best_match_typo(self):
        """Test when command has a typo"""
        result = _find_best_match("ad contact", self.valid_commands)
        self.assertEqual(result, "add contact")
    
    def test_find_best_match_multi_word_base(self):
        """Test with multi-word command base"""
        result = _find_best_match("show al", self.valid_commands)
        self.assertEqual(result, "show all contacts")
    
    def test_find_best_match_no_match(self):
        """Test when no match is found"""
        result = _find_best_match("xyz unknown", self.valid_commands)
        self.assertIsNone(result)
    
    def test_find_best_match_empty_command(self):
        """Test with empty command"""
        result = _find_best_match("", self.valid_commands)
        # Empty string matches as prefix of all commands, returns first one
        self.assertEqual(result, "add contact")
    
    def test_find_best_match_case_insensitive(self):
        """Test that matching is case insensitive"""
        result = _find_best_match("ADD CONTACT", self.valid_commands)
        self.assertEqual(result, "add contact")


class TestHandleCommandWithGuess(unittest.TestCase):
    """Test cases for handle_command_with_guess function"""
    
    def setUp(self):
        self.valid_commands = ["add contact", "edit contact", "show contact"]
        self.handler = MagicMock()
        self.general_callback = MagicMock()
        self.handler_args = ("test_arg",)
    
    def test_handle_show_birthdays_special_case(self):
        """Test special handling for 'show birthdays' command"""
        handle_command_with_guess(
            "show birthdays 7", 
            self.valid_commands, 
            self.handler, 
            *self.handler_args
        )
        self.handler.assert_called_once_with("show birthdays 7", "test_arg")
    
    def test_handle_exact_command_match(self):
        """Test when command exactly matches a valid command"""
        handle_command_with_guess(
            "add contact", 
            self.valid_commands, 
            self.handler, 
            *self.handler_args
        )
        self.handler.assert_called_once_with("add contact", "test_arg")
    
    @patch('builtins.input', return_value='y')
    @patch('builtins.print')
    def test_handle_fuzzy_match_user_accepts(self, mock_print, mock_input):
        """Test when user accepts the suggested command"""
        handle_command_with_guess(
            "ad contact", 
            self.valid_commands, 
            self.handler, 
            *self.handler_args
        )
        
        # Should prompt user
        mock_print.assert_called_with("Можливо, ви мали на увазі: 'add contact'? (y/n)")
        # Should call handler with corrected command
        self.handler.assert_called_once_with("add contact", "test_arg")
    
    @patch('builtins.input', return_value='n')
    @patch('builtins.print')
    def test_handle_fuzzy_match_user_rejects(self, mock_print, mock_input):
        """Test when user rejects the suggested command"""
        handle_command_with_guess(
            "ad contact", 
            self.valid_commands, 
            self.handler, 
            *self.handler_args
        )
        
        # Should prompt user and show error
        expected_calls = [
            call("Можливо, ви мали на увазі: 'add contact'? (y/n)"),
            call("⚠️ Невідома команда для контактів.")
        ]
        mock_print.assert_has_calls(expected_calls)
        # Should not call handler
        self.handler.assert_not_called()
    
    @patch('builtins.input', return_value='y')
    @patch('builtins.print')
    def test_handle_fuzzy_match_general_command_accepted(self, mock_print, mock_input):
        """Test when suggested command is a general command and user accepts"""
        valid_commands_with_general = self.valid_commands + GENERAL_COMMANDS
        
        result = handle_command_with_guess(
            "hel", 
            valid_commands_with_general, 
            self.handler, 
            *self.handler_args,
            general_command_callback=self.general_callback
        )
        
        # Should call general callback instead of handler
        self.general_callback.assert_called_once_with("help")
        self.handler.assert_not_called()
    
    def test_handle_general_command_direct(self):
        """Test when command is directly a general command"""
        valid_commands_with_general = self.valid_commands + GENERAL_COMMANDS
        
        result = handle_command_with_guess(
            "help", 
            valid_commands_with_general, 
            self.handler, 
            *self.handler_args,
            general_command_callback=self.general_callback
        )
        
        # Should call general callback
        self.general_callback.assert_called_once_with("help")
        self.handler.assert_not_called()
    
    def test_handle_general_command_no_callback(self):
        """Test general command when no callback is provided"""
        valid_commands_with_general = self.valid_commands + GENERAL_COMMANDS
        
        result = handle_command_with_guess(
            "help", 
            valid_commands_with_general, 
            self.handler, 
            *self.handler_args
        )
        
        # Should not call handler or callback
        self.handler.assert_not_called()
        self.assertIsNone(result)
    
    def test_handle_no_match_found(self):
        """Test when no match is found for the command"""
        handle_command_with_guess(
            "unknown command", 
            self.valid_commands, 
            self.handler, 
            *self.handler_args
        )
        
        # Should call handler with original command
        self.handler.assert_called_once_with("unknown command", "test_arg")


if __name__ == '__main__':
    unittest.main()