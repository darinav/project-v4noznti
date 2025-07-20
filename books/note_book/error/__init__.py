# -*- coding: utf-8 -*-

__title__ = 'Notebook errors and exceptions'
__author__ = 'project-group-3'


from .exceptions import (
    NoteNotFound,
    NoteAlreadyExist,
    NoteTitleMandatory,
    NoteTextMandatory,
    TagValueCannotBeEmpty,
)

__all__ = [
    'NoteNotFound',
    'NoteAlreadyExist',
    'NoteTitleMandatory',
    'NoteTextMandatory',
    'TagValueCannotBeEmpty',
]
