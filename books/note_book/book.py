# -*- coding: utf-8 -*-

"""
Note Book class implementation
"""

import enum
from collections import UserList


from .error import NoteNotFound, NoteAlreadyExist
from .note import Note


class NoteBook(UserList):

    class SortOrder(enum.Enum):
        index = enum.auto()
        title = enum.auto()
        tags = enum.auto()

    def __init__(self, *args, unique_titles: bool = False):
        """ Initialize a Note Book with the specified Notes, if given

        :param args: the note records (Note, optional)
        :param unique_titles: the note title must be unique (boolean, optional)
        """
        super().__init__()
        self.__unique_titles: bool = unique_titles
        # Add note records if given, removing duplicates
        for note in args:
            if not self.__unique_titles or note.title not in self.__titles():
                self.add_note(note)

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, value):
        self.__dict__ = value

    def __titles(self) -> set[str]:
        """ Return the notes titles

        :return: set of the notes titles (set of str)
        """
        return {n.title for n in self.data}

    def notes(self, order: SortOrder = SortOrder.index) -> list[tuple[int, Note]]:
        """ Return the sorted notes with indices

        :param order: the note sort order rule (SortOrder, optional)
        :return: list of the note records (list of tuple int, Note)
        """
        if order == NoteBook.SortOrder.index:
            return [(idx + 1, n) for idx, n in enumerate(self.data)]

        return [
            (self.data.index(n) + 1, n) for n in sorted(
                self.data,
                key=lambda i: (i.tags if order == NoteBook.SortOrder.tags else i.title).lower()
            )
        ]

    def add_note(self, note: Note) -> None:
        """ Add the note record, or raise the note already exists exception

        :param note: note record (Note, mandatory)
        """
        if self.__unique_titles and note.title in self.__titles():
            # Unique titles mode: Note found - raise the note already exists exception
            raise NoteAlreadyExist()
        # Add the note record
        self.data.append(note)

    def get_note(self, index: int) -> Note:
        """ Get the note record, or raise the note not found exception

        :param index: note record (Note, mandatory)
        """
        if index <= 0:
            # Wrong index value - raise the note not found exception
            raise NoteNotFound()
        # Remove the note
        try:
            return self.data[index-1]
        except IndexError:
            raise NoteNotFound()

    def delete_note(self, index: int) -> None:
        """ Remove the note record, or raise the note not found exception

        :param index: note index (int, mandatory)
        """
        if index <= 0:
            # Wrong index value - raise the note not found exception
            raise NoteNotFound()
        # Remove the note
        try:
            self.data.pop(index-1)
        except IndexError:
            raise NoteNotFound()

    def __search_merge(self, *args) -> list[tuple[int, Note]]:
        """ Merge search result sets and return the notes with indices

        :param args: search result sets (set of string, optional)
        :return: found notes (list of tuple int, Note)
        """
        found_indices: set[int] = set()
        # Combine the search results into a single set
        for result in args:
            if isinstance(result, set):
                found_indices.update(result)
        # Return found notes
        return [(i, self.data[i]) for i in found_indices if i < len(self.data)]

    def search_by_title(self, keyword: str) -> list[tuple[int, Note]]:
        """ Search and return the notes with indices by keyword/sequence in the title

        :param keyword: search keyword or sequence (string, mandatory)
        :return: found notes (list of tuple int, Note)
        """
        # Return the found notes
        return self.__search_merge({idx for idx, n in enumerate(self.data) if keyword and keyword in n.title})

    def search_by_text(self, keyword: str) -> list[tuple[int, Note]]:
        """ Search and return the notes with indices by keyword/sequence in the text

        :param keyword: search keyword or sequence (string, mandatory)
        :return: found notes (list of tuple int, Note)
        """
        # Return the found notes
        return self.__search_merge({idx for idx, n in enumerate(self.data) if keyword and keyword in n.text})

    def search_by_tag(self, keyword: str) -> list[tuple[int, Note]]:
        """ Search and return the notes with indices by keyword/sequence in the tags

        :param keyword: search keyword or sequence (string, mandatory)
        :return: found notes (list of tuple int, Note)
        """
        # Return the found notes
        return self.__search_merge(
            {idx for idx, n in enumerate(self.data) if keyword and keyword in n.tags}
        )

    def search(self, keyword: str) -> list[tuple[int, Note]]:
        """ Search and return the notes with indices by keyword/sequence in the title, text and tags

        :param keyword: search keyword or sequence (string, mandatory)
        :return: found notes (list of tuple int, Note)
        """
        # Return the found notes
        return self.__search_merge(
            {idx for idx, n in enumerate(self.data) if keyword and keyword in n.title},
            {idx for idx, n in enumerate(self.data) if keyword and keyword in n.text},
            {idx for idx, n in enumerate(self.data) if keyword and keyword in n.tags},
        )
