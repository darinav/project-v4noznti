import unittest
from unittest.mock import patch, MagicMock

from cli.guess_command.guess_command import handle_command_with_guess, _suggest_command as suggest_command
from cli.guess_command.possible_commands import CONTACT_COMMANDS, NOTE_COMMANDS

class TestSuggestCommand(unittest.TestCase):
    def test_exact_match(self):
        self.assertEqual(suggest_command("add contact", CONTACT_COMMANDS), "add contact")
        self.assertEqual(suggest_command("delete contact", CONTACT_COMMANDS), "delete contact")
        self.assertEqual(suggest_command("add note", NOTE_COMMANDS), "add note")
        self.assertEqual(suggest_command("delete note", NOTE_COMMANDS), "delete note")

    def test_fuzzy_match(self):
        self.assertEqual(suggest_command("ad contact", CONTACT_COMMANDS), "add contact")
        self.assertEqual(suggest_command("shw contact", CONTACT_COMMANDS), "show contact")
        self.assertEqual(suggest_command("ad note", NOTE_COMMANDS), "add note")
        self.assertEqual(suggest_command("show nt", NOTE_COMMANDS), "show all notes")


class TestHandleCommandWithGuess(unittest.TestCase):
    def test_exact_command_runs_handler(self):
        handler = MagicMock()
        handle_command_with_guess("add contact Vasya", CONTACT_COMMANDS, handler)
        handler.assert_called_with("add contact Vasya")

    @patch('builtins.input', return_value='y')
    def test_fuzzy_command_with_user_accepts(self, mock_input):
        handler = MagicMock()
        handle_command_with_guess("ad contact Vasya", CONTACT_COMMANDS, handler)
        handler.assert_called_with("add contact Vasya")

    @patch('builtins.input', return_value='n')
    def test_fuzzy_command_with_user_rejects(self, mock_input):
        handler = MagicMock()
        handle_command_with_guess("ad contact Vasya", CONTACT_COMMANDS, handler)
        handler.assert_not_called()

if __name__ == "__main__":
    unittest.main()
