# -*- coding: utf-8 -*-

"""
Note Book class implementation
"""

import enum
from collections import UserDict


from .error import NoteNotFound, NoteAlreadyExist
from .note import Note


class NoteBook(UserDict):

    class SortOrder(enum.Enum):
        title = enum.auto()
        tags = enum.auto()

    def __init__(self, *args):
        """ Initialize a Note Book with the specified Notes, if given

        :param args: the note records (Note, optional)
        """
        super().__init__()
        # Add note records if given, removing duplicates
        for note in args:
            if str(note.title) not in self:
                self.add_note(note)

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, value):
        self.__dict__ = value

    def notes(self, order: SortOrder = SortOrder.title) -> list[Note]:
        """ Return the sorted note records

        :param order: the note sort order rule (SortOrder, optional)
        :return: list of the note records (list of Note)
        """
        return sorted(self.values(), key=lambda n: (n.tags if order == NoteBook.SortOrder.tags else n.title).lower())

    def find(self, title: str) -> Note:
        """ Search and return the note record, or raise the not found exception

        :param title: the note title (string, mandatory)
        :return: the note record, if found (Note)
        """
        if title not in self:
            # Note not found - raise the note not found exception
            raise NoteNotFound()
        # Return the contact
        return self.get(title, None)

    def add_note(self, note: Note) -> None:
        """ Add the note record, or raise the note already exists exception

        :param note: note record (Note, mandatory)
        """
        if note.title in self:
            # Note found - raise the note already exists exception
            raise NoteAlreadyExist()
        # Add the note record
        self.data[note.title] = note

    def delete_note(self, title: str) -> None:
        """ Remove the note record, or raise the note not found exception

        :param title: note title (string, mandatory)
        """
        if title not in self:
            # Note not found - raise the note not found exception
            raise NoteNotFound()
        # Remove the note record
        self.pop(title, None)
