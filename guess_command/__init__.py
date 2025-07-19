# -*- coding: utf-8 -*-
"""
Пакет guess_command — підказка команд для CLI-помічника.
"""

from .guess_command import handle_command_with_guess
from .possible_commands import CONTACT_COMMANDS, NOTE_COMMANDS

__all__ = [
    "handle_command_with_guess",
    "CONTACT_COMMANDS",
    "NOTE_COMMANDS",
]