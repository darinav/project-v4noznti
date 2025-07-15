# -*- coding: utf-8 -*-"

"""
Exceptions for address book implementation
"""

from books.commons import ObjectNotFound, ObjectAlreadyExist, ObjectValueError


class ContactNotFound(ObjectNotFound):
    def __init__(self):
        super().__init__("The contact not found")


class ContactAlreadyExist(ObjectAlreadyExist):
    def __init__(self):
        super().__init__("The contact already exists")


class ContactNameMandatory(ObjectValueError):
    def __init__(self):
        super().__init__("The contact name is required")


class ContactPhoneNotFound(ObjectNotFound):
    def __init__(self):
        super().__init__("The contact phone number not found")


class ContactPhoneAlreadyExist(ObjectAlreadyExist):
    def __init__(self):
        super().__init__("The contact phone number already exists")


class ContactPhoneValueError(ObjectValueError):
    def __init__(self):
        super().__init__(
            "The contact phone number must be a valid phone number in international format"
        )


class ContactEmailNotFound(ObjectNotFound):
    def __init__(self):
        super().__init__("The contact email not found")


class ContactEmailAlreadyExist(ObjectAlreadyExist):
    def __init__(self):
        super().__init__("The contact email already exists")


class ContactEmailValueError(ObjectValueError):
    def __init__(self):
        super().__init__("The contact email must be a valid email address")


class ContactBirthdayAlreadyExist(ObjectAlreadyExist):
    def __init__(self):
        super().__init__("The contact birthday already exists")


class ContactBirthdayValueError(ObjectValueError):
    def __init__(self):
        super().__init__("The contact birthday must be in \"DD.MM.YYYY\" format")
