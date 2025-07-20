# -*- coding: utf-8 -*-

__title__ = 'Address book errors and exceptions'
__author__ = 'project-group-3'


from .exceptions import (
    ContactNotFound,
    ContactAlreadyExist,
    ContactNameMandatory,
    ContactPhoneNotFound,
    ContactPhoneAlreadyExist,
    ContactPhoneValueError,
    ContactEmailNotFound,
    ContactEmailAlreadyExist,
    ContactEmailValueError,
    ContactBirthdayAlreadyExist,
    ContactBirthdayValueError,
    ContactAddressAlreadyExist,
    ContactAddressCannotBeEmpty,
)

__all__ = [
    'ContactNotFound',
    'ContactAlreadyExist',
    'ContactNameMandatory',
    'ContactPhoneNotFound',
    'ContactPhoneAlreadyExist',
    'ContactPhoneValueError',
    'ContactEmailNotFound',
    'ContactEmailAlreadyExist',
    'ContactEmailValueError',
    'ContactBirthdayAlreadyExist',
    'ContactBirthdayValueError',
    'ContactAddressAlreadyExist',
    'ContactAddressCannotBeEmpty',
]
