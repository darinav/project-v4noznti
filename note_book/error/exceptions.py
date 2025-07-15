# -*- coding: utf-8 -*-"

"""
Exceptions for notebook implementation
"""


class ObjectNotFound(KeyError):
    def __init__(self, message):
        super().__init__(message)


class ObjectAlreadyExist(KeyError):
    def __init__(self, message):
        super().__init__(message)


class ObjectValueError(ValueError):
    def __init__(self, message):
        super().__init__(message)


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
