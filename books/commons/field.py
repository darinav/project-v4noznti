# -*- coding: utf-8 -*-

"""
Field class for the book classes implementation
"""

from typing import Any


class Field:
    """
    Immutable class that can be used in Set and Dict key
    """

    def __init__(self, value: Any):
        """ Initialize the field with the specified value

        :param value: the value (any types, mandatory)
        """
        super().__setattr__('_protected_value', value)

    def __str__(self) -> str:
        """ Create a readable string for the class instance

        :return: readable string (string)
        """
        return str(self.value)

    def __setattr__(self, key, value):
        raise AttributeError("Class is immutable")

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, Field) and self.value == other.value

    @property
    def value(self) -> Any:
        return super().__getattribute__('_protected_value')

