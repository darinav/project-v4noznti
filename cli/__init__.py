"""
CLI package for the personal assistant application.

This package contains the command-line interface modules:
- cli: Main CLI interface
- contact_commands: Contact management commands
- note_commands: Note management commands
"""

from .cli import main, print_main_menu, print_help
from .contact_commands import handle_contact_command
from .note_commands import handle_note_command

__all__ = [
    'main',
    'print_main_menu', 
    'print_help',
    'handle_contact_command',
    'handle_note_command'
]