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
        for note in args:
            if not self.__unique_titles or note.title not in self.__titles():
                self.add_note(note)

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, value):
        self.__dict__ = value

    def __next_note_index(self) -> int:
        """ Return the next Note index

        :return: index (int)
        """
        return max(self.keys()) + 1 if self.data else 1

    def __titles(self) -> set[str]:
        """ Return the notes titles

        :return: set of the notes titles (set of str)
        """
        return {n.title for n in self.data.values()}

    def notes(self, order: SortOrder = SortOrder.index) -> list[tuple[int, Note]]:
        """ Return the sorted notes with indices

        :param order: the note sort order rule (SortOrder, optional)
        :return: list of the note records (list of tuple int, Note)
        """
        if order != NoteBook.SortOrder.index:
            return [
                (idx, note) for idx, note in sorted(
                    self.items(),
                    key=lambda item: (item[1].tags if order == NoteBook.SortOrder.tags else item[1].title).lower()
                )
            ]

        return [(idx, note) for idx, note in self.items()]

    def add_note(self, note: Note) -> int:
        """ Add the note record, or raise the note already exists exception

        :param note: note record (Note, mandatory)
        :return: index of the added note (int)
        """
        if self.__unique_titles and note.title in self.__titles():
            raise NoteAlreadyExist()
        self.data[self.__next_note_index()] = note
        return next(reversed(self.data))

    def get_note(self, index: int) -> tuple[int, Note]:
        """ Get the note record, or raise the note not found exception

        :param index: note record index (int, mandatory)
        :return: note record with index (tuple int, Note)
        """
        if index <= 0:
            raise NoteNotFound()
        try:
            return index, self.data[index]
        except KeyError:
            raise NoteNotFound()

    def delete_note(self, index: int) -> None:
        """ Remove the note record, or raise the note not found exception

        :param index: note index (int, mandatory)
        """
        if index <= 0:
            raise NoteNotFound()
        try:
            self.data.pop(index)
        except KeyError:
            raise NoteNotFound()

    def __search_merge(self, *args) -> list[tuple[int, Note]]:
        """ Merge search result sets and return the notes with indices

        :param args: search result sets (set of string, optional)
        :return: found notes (list of tuple int, Note)
        """
        found_keys: set[str] = set()
        for result in args:
            if isinstance(result, set):
                found_keys.update(result)
        return [(idx, note) for idx, note in self.data.items() if idx in found_keys]

    def search_by_title(self, keyword: str) -> list[tuple[int, Note]]:
        """ Search and return the notes with indices by keyword/sequence in the title

        :param keyword: search keyword or sequence (string, mandatory)
        :return: found notes (list of tuple int, Note)
        """
        keyword = keyword.lower() or ""
        return self.__search_merge(
            {idx for idx, note in self.data.items() if keyword and keyword in note.title.lower()}
        )

    def search_by_text(self, keyword: str) -> list[tuple[int, Note]]:
        """ Search and return the notes with indices by keyword/sequence in the text

        :param keyword: search keyword or sequence (string, mandatory)
        :return: found notes (list of tuple int, Note)
        """
        keyword = keyword.lower() or ""
        return self.__search_merge(
            {idx for idx, note in self.data.items() if keyword and keyword in note.text.lower()}
        )

    def search_by_tag(self, keyword: str) -> list[tuple[int, Note]]:
        """ Search and return the notes with indices by keyword/sequence in the tags

        :param keyword: search keyword or sequence (string, mandatory)
        :return: found notes (list of tuple int, Note)
        """
        keyword = keyword.lower() or ""
        return self.__search_merge(
            {idx for idx, note in self.data.items() if keyword and keyword in note.tags.lower()}
        )

    def search(self, keyword: str) -> list[tuple[int, Note]]:
        """ Search and return the notes with indices by keyword/sequence in the title, text and tags

        :param keyword: search keyword or sequence (string, mandatory)
        :return: found notes (list of tuple int, Note)
        """
        keyword = keyword.lower() or ""
        return self.__search_merge(
            {idx for idx, note in self.data.items() if keyword and keyword in note.title.lower()},
            {idx for idx, note in self.data.items() if keyword and keyword in note.text.lower()},
            {idx for idx, note in self.data.items() if keyword and keyword in note.tags.lower()},
        )
