# -*- coding: utf-8 -*-"

"""
Note class for notebook implementation
"""

import re
from typing import Optional, Any


from ..error import (
    NoteTitleMandatory,
    NoteTextMandatory,
)


class Field:
    def __init__(self, value: Any):
        """ Initialize the field with the specified value

        :param value: the value (any type, mandatory)
        """
        self.value = value

    def __str__(self) -> str:
        """ Create a readable string for the class instance

        :return: readable string (string)
        """
        return str(self.value)


class Title(Field):
    def __init__(self, value: Any):
        """ Initialize the Title field with the specified value

        :param value: the value (any type, mandatory)
        """
        # Check whether the name is empty or None
        if not value:
            raise NoteTitleMandatory()
        super().__init__(str(value))


class Text(Field):
    def __init__(self, value: Any):
        """ Initialize the Text field with the specified value

        :param value: the value (any type, mandatory)
        """
        # Check whether the name is empty or None
        if not value:
            raise NoteTextMandatory()
        super().__init__(str(value))


class Tags:
    hash_tag_search_pattern = re.compile(r'#(?P<tag>\w+)')

    def __init__(self, tags: Optional[list[Any]] = None):
        """ Initialize the tags with the specified list of tags or an empty tags list

        :param tags: list of tags (list of any values, optional)
        """
        self.__tags: set[str] = {str(tag) for tag in (tags or []) if tag is not None or str(tag) != ''}

    def __str__(self) -> str:
        """ Create a readable string for the class instance

        :return: readable string (string)
        """
        return ', '.join(sorted(self.__tags))

    @property
    def count(self) -> int:
        return len(self.__tags)


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
        self.__tags = Tags(tags=tags if tags else (self.__class__.parse_text_for_hashtags(text ) if hashtags else None))


    def __str__(self) -> str:
        """ Create a readable string for the class instance

        :return: readable string (string)
        """

        readable_string: str = f"Note title: {self.title}; text: {self.text}"
        if self.__tags.count > 0:
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
        return str(self.__tags)

    @classmethod
    def parse_text_for_hashtags(cls, text: str) -> list[str]:
        """ Parse the text for tags and return tags list

        :param text: the text for parsing (string, mandatory)
        :return: list of the found tags (list of string)
        """
        return list(set(re.findall(Tags.hash_tag_search_pattern, text))) if text else []