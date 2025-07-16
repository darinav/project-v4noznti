# -*- coding: utf-8 -*-

"""
Common exceptions for the book classes implementation
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
