# -*- coding: utf-8 -*-

"""
Note class for notebook implementation
"""

from __future__ import annotations

import re
from typing import Optional, Any
from collections.abc import Iterator

from books.commons import Field
from ..error import NoteTitleMandatory, NoteTextMandatory, TagValueCannotBeEmpty


class Title(Field):
    def __init__(self, value: str):
        """ Initialize the Title field with the specified value

        :param value: the title (string, mandatory)
        """
        # Check whether the name is empty or None
        if not value:
            raise NoteTitleMandatory()
        super().__init__(str(value))


class Text(Field):
    def __init__(self, value: str):
        """ Initialize the Text field with the specified value

        :param value: the text (string, mandatory)
        """
        # Check whether the name is empty or None
        if not value:
            raise NoteTextMandatory()
        super().__init__(str(value))


class Tag(Field):
    def __init__(self, value: str):
        """ Initialize the Tag field with the specified value

        :param value: the text (string, mandatory)
        """
        # Check whether the name is empty or None
        if not value:
            raise TagValueCannotBeEmpty()
        super().__init__(str(value))


class Tags:
    hash_tag_search_pattern = re.compile(r'#(?P<tag>\w+)')

    def __init__(self, *args):
        """ Initialize the tags with the specified list of tags or an empty tags list

        :param args: tuple of tags (tuple of any values, optional)
        """
        self.__tags: set[Tag] = {Tag(tag) for tag in args if tag is not None and str(tag) != ''}

    def __str__(self) -> str:
        """ Create a readable string for the class instance

        :return: readable string (string)
        """
        return ', '.join(sorted([str(t) for t in self.__tags]))

    def __iter__(self) -> Iterator[Tag]:
        """ Iterables on the existing tags

        :return: Tags iterator (Iterator)
        """
        return iter(self.__tags)

    def __contains__(self, value: Any) -> bool:
        return self.__find(value) is not None

    def __len__(self) -> int:
        """ Return the number of the existing tags

        :return: number of the existing tags (int)
        """
        return len(self.__tags)

    def __add__(self, tags: Tags) -> Tags:
        """ Add the new tags to the existing ones

        :param tags: new tags (Tags, optional)
        :return: current instance (Tags)
        """
        self.__tags.update(tags)
        return self

    def __radd__(self, tags: Tags) -> Tags:
        """ Add the new tags to the existing ones

        :param tags: new tags (Tags, optional)
        :return: current instance (Tags)
        """
        return self.__add__(tags)

    def __sub__(self, tags: Tags) -> Tags:
        """ Remove the tags from the existing ones

        :param tags: tags to be deleted (Tags, optional)
        :return: current instance (Tags)
        """
        self.__tags.difference_update(tags)
        return self

    def __rsub__(self, tags: Tags) -> Tags:
        """ Remove the tags from the existing ones

        :param tags: tags to be deleted (Tags, optional)
        :return: current instance (Tags)
        """
        return self.__sub__(tags)

    def __find(self, value: Any) -> Optional[Tag]:
        """ Private method for searching the Tag by value

        :param value: tag value (any type, mandatory)
        :return: Tag field, if found (Tag, optional)
        """
        # Find and return by tag value
        return next((tag for tag in self if str(tag) == str(value)), None)


class Note:
    def __init__(self, title: str, text: str, tags: Optional[list[Any]] = None, hashtags: bool = True):
        """ Initialize the Note record for the specified Title and with the Text, and Tags (if given)

        :param title: the title of the note (string, mandatory)
        :param text: the text of the note (string, mandatory)
        :param tags: the tags list for the note (list of any values, optional)
        :param tags: parse the note text for hashtags (bool, optional)
        """
        self.__title = Title(title)
        self.__text = Text(text)
        self.__tags = Tags()
        if tags and isinstance(tags, list):
            self.__tags += Tags(*tags)
        if hashtags:
            self.__tags += Tags(*self.__class__.parse_text_for_hashtags(text))


    def __str__(self) -> str:
        """ Create a readable string for the class instance

        :return: readable string (string)
        """

        readable_string: str = f"Note title: {self.title}; text: {self.text}"
        if self.tags_number > 0:
            readable_string += f"; tags: {self.tags}"
        return readable_string

    @property
    def title(self) -> str:
        return str(self.__title)

    @property
    def text(self) -> str:
        return str(self.__text)

    @property
    def tags(self) -> str:
        """ Return the all existing tags

        :return: all tags lexicographically sorted in string representation (string)
        """
        return str(self.__tags)

    @property
    def tags_number(self) -> int:
        """ Return the number of the existing tags

        :return: number of the existing tags (int)
        """
        return len(self.__tags)

    @classmethod
    def parse_text_for_hashtags(cls, text: str) -> list[str]:
        """ Parse the text for tags and return tags list

        :param text: the text for parsing (string, mandatory)
        :return: list of the found tags (list of string)
        """
        return list(set(re.findall(Tags.hash_tag_search_pattern, text))) if text else []

    def add_tags(self, *args) -> str:
        """ Add the new tags to the existing ones

        :param args: tag values (any type, optional)
        :return: all tags lexicographically sorted in string representation (string)
        """
        self.__tags += Tags(*args)
        return self.tags

    def delete_tags(self, *args) -> str:
        """ Remove the tags from the existing ones

        :param args: tag values (any type, optional)
        :return: all tags lexicographically sorted in string representation (string)
        """
        self.__tags -= Tags(*args)
        return self.tags

    def replace_tags(self, *args) -> str:
        """ Replace the existing tags with new ones

        :param args: tag values (any type, optional)
        :return: all tags lexicographically sorted in string representation (string)
        """
        self.__tags = Tags(*args)
        return self.tags

    def is_tag_exist(self, value: Any) -> bool:
        """ Check if the tag with the specified value exists

        :param value: tag value (any type, mandatory)
        :return: flag indicating whether the tag exists (boolean)
        """
        # Find a tag and return a flag indicating whether the tag exists
        return value in self.__tags

    def edit_title(self, title: str) -> None:
        """ Replace the Note record Title with the specified one

        :param title: the title of the note (string, mandatory)
        """
        self.__title = Title(title)

    def edit_text(self, text: str) -> None:
        """ Replace the Note record Text with the specified one

        :param text: the text of the note (string, mandatory)
        """
        # Remove the old Text tags
        self.delete_tags(*self.__class__.parse_text_for_hashtags(self.__text.value))
        # Replace text
        self.__text = Text(text)
        # Add the new Text tags
        self.add_tags(*self.__class__.parse_text_for_hashtags(self.__text.value))
