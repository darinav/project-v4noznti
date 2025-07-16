# -*- coding: utf-8 -*-

__title__ = 'Personal Assistant Books Base Classes'
__author__ = 'project-group-3'

import books.address_book.error as address_book_errors
from books.address_book import AddressBook, Record
import books.note_book.error as note_book_errors
from books.note_book import NoteBook, Note

__all__ = ['AddressBook', 'Record', 'address_book_errors', 'NoteBook', 'Note', 'note_book_errors']
