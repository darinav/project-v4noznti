# -*- coding: utf-8 -*-"

"""
Exceptions for notebook implementation
"""

from books.commons import ObjectNotFound, ObjectAlreadyExist, ObjectValueError


class NoteNotFound(ObjectNotFound):
    def __init__(self):
        super().__init__("The note not found")


class NoteAlreadyExist(ObjectAlreadyExist):
    def __init__(self):
        super().__init__("The note with same title already exists")


class NoteTitleMandatory(ObjectValueError):
    def __init__(self):
        super().__init__("The note title is required")


class NoteTextMandatory(ObjectValueError):
    def __init__(self):
        super().__init__("The note text is required")


class TagValueCannotBeEmpty(ObjectValueError):
    def __init__(self):
        super().__init__("The tag value cannot be empty")
