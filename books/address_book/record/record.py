# -*- coding: utf-8 -*-

"""
Record class for address book implementation
"""

import re
import datetime
import phonenumbers
from typing import Optional


from books.commons import Field
from ..error import (
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


class Name(Field):
    def __init__(self, value: str):
        """ Initialize the Name field with the specified value

        :param value: the value (string, mandatory)
        """
        if not value:
            raise ContactNameMandatory()
        super().__init__(str(value))


class Birthday(Field):
    def __init__(self, value: str):
        """ Initialize the Birthday field with the specified value

        :param value: the value (string, mandatory)
        """
        super().__init__(self.prepare(value))

    def __str__(self) -> str:
        """ Create a readable string for the Birthday class instance

        :return: readable string (string)
        """
        return self.value.strftime("%d.%m.%Y") if self.value else ''

    @classmethod
    def prepare(cls, value: str) -> datetime.date:
        """ Birthday validation and conversion

        :param value: birthday string (string, mandatory)
        :return: birthday (datetime)
        """
        try:
            return datetime.datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ContactBirthdayValueError()

    def date_of_birth(self) -> datetime.date:
        """Return the date of birth.

        :return: Date of birth (date)
        """
        return self.value

    def birthday(self, year: int) -> datetime.date:
        """Return the anniversary of the birth shifted to the specified year. If the date is on February 29 and
        today's year is not a leap year, move it to March 1.

        :param year: Year to which the date should be shifted (int, mandatory)
        :return: Date shifted to the specified year (date)
        """
        try:
            return self.value.replace(year=year)
        except ValueError:
            return datetime.date(year, 3, 1)


class Phone(Field):
    strict: bool = False
    value_clear_pattern = re.compile(r"\D")

    def __init__(self, value: str):
        """ Initialize the Phone number field with the specified value

        :param value: the value (string, mandatory)
        """
        super().__init__(self.prepare(value))

    @classmethod
    def prepare(cls, value: str) -> str:
        """ Phone number validation and sanitization

        :param value: phone number (string, mandatory)
        :return: sanitized phone number (string)
        """

        if not value:
            raise ContactPhoneValueError()
        value = '+' + re.sub(cls.value_clear_pattern, '', value)
        try:
            phone_number = phonenumbers.parse(value)
            if (
                    not phonenumbers.is_valid_number(phone_number)
                    and
                    (cls.strict or not phonenumbers.is_possible_number(phone_number))
            ):
                raise ContactPhoneValueError()
            value = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            raise ContactPhoneValueError()
        return value


class Email(Field):
    value_clear_pattern = re.compile(r"\s")
    value_match_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    def __init__(self, value: str):
        """ Initialize the Email field with the specified value

        :param value: the value (string, mandatory)
        """
        super().__init__(self.prepare(value))

    @classmethod
    def prepare(cls, value: str) -> str:
        """ Email number validation and sanitization

        :param value: email (string, mandatory)
        :return: sanitized email (string)
        """

        if not value:
            raise ContactEmailValueError()
        value = re.sub(cls.value_clear_pattern, '', value)
        if not re.match(cls.value_match_pattern, value):
            raise ContactEmailValueError()
        return value


class Address(Field):
    def __init__(self, value: str):
        """ Initialize the Address field with the specified value

        :param value: the value (string, mandatory)
        """
        if not value:
            raise ContactAddressCannotBeEmpty()
        super().__init__(str(value))


class Record:
    def __init__(
            self,
            name: str,
            address: Optional[str] = None,
            birthday: Optional[str] = None,
            phones: Optional[list[str]] = None,
            emails: Optional[list[str]] = None,
    ):
        """ Initialize the Contact record for the specified Name and with the Address, Birthday, Phone numbers
            or Emails, if given

        :param name: the name value (string, mandatory)
        :param address: the address value (string, optional)
        :param birthday: the birthday value (string, optional)
        :param phones: the phone numbers (list of strings, optional)
        :param emails: the emails (list of strings, optional)
        """
        self.__name: Name = Name(name)
        self.__address: Optional[Address] = None
        self.__birthday: Optional[Birthday] = None
        self.__phones: list[Phone] = []
        self.__emails: list[Email] = []
        if isinstance(address, str) and address:
            self.edit_address(address)
        if isinstance(birthday, str) and birthday:
            self.edit_birthday(birthday)
        if isinstance(phones, list):
            for phone in phones:
                if self.__find_phone(phone) is None:
                    self.add_phone(phone)
        if isinstance(emails, list):
            for email in emails:
                if self.__find_email(email) is None:
                    self.add_email(email)

    def __str__(self) -> str:
        """ Create a readable string for the class instance

        :return: readable string (string)
        """

        readable_string: str = f"Contact name: {self.name}"
        if self.__birthday is not None:
            readable_string += f", birthday: {str(self.birthday)}"
        if self.__phones:
            readable_string += ", phones: {phones}".format(phones="; ".join(i for i in self.phones))
        if self.__emails:
            readable_string += ", emails: {emails}".format(emails="; ".join(i for i in self.emails))
        if self.__address:
            readable_string += f", address: {self.address}"
        return readable_string

    @property
    def name(self) -> str:
        return str(self.__name)

    @property
    def address(self) -> str:
        return str(self.__address) if self.__address is not None else ''

    @property
    def birthday(self) -> Optional[datetime.date]:
        return self.__birthday

    @property
    def phones(self) -> list[str]:
        return [str(i) for i in self.__phones]

    @property
    def emails(self) -> list[str]:
        return [str(i) for i in self.__emails]

    def __find_phone(self, phone: str) -> Optional[Phone]:
        """ Private method for searching the phone number

        :param phone: phone number (string, mandatory)
        :return: phone field, if found (Phone, optional)
        """
        phone = Phone.prepare(phone)
        return next((p for p in self.__phones if p.value == phone), None)

    def __find_email(self, email: str) -> Optional[Email]:
        """ Private method for searching the email

        :param email: email (string, mandatory)
        :return: email field, if found (Email, optional)
        """
        email = Email.prepare(email)
        return next((p for p in self.__emails if p.value == email), None)

    def edit_name(self, name: str) -> None:
        """ Edit the name, or raise the name value mandatory exception

        :param name: contact`s name (string, mandatory)
        """
        self.__name = Name(name)

    def add_address(self, address: str) -> None:
        """ Add the address to the Contact record, or raise the address already exists exception

        :param address: address string (string, mandatory)
        """
        if self.__address is not None:
            raise ContactAddressAlreadyExist()
        self.edit_address(address)

    def edit_address(self, address: str) -> None:
        """ Edit the address for the Contact record, or raise the address value error exception

        :param address: address string (string, mandatory)
        """
        self.__address = Address(address)

    def delete_address(self) -> None:
        """ Delete the address from the Contact record
        """
        self.__address = None

    def add_birthday(self, birthday: str) -> None:
        """ Add the birthday to the Contact record, or raise the birthday already exists exception

        :param birthday: birthday (string, mandatory)
        """
        if self.__birthday is not None:
            raise ContactBirthdayAlreadyExist()
        self.edit_birthday(birthday)

    def edit_birthday(self, birthday: str) -> None:
        """ Edit the birthday for the Contact record, or raise the birthday value error exception

        :param birthday: birthday (string, mandatory)
        """
        self.__birthday = Birthday(birthday)

    def delete_birthday(self) -> None:
        """ Delete the birthday from the Contact record
        """
        self.__birthday = None

    def next_birthday(self, today: datetime.date) -> Optional[datetime.date]:
        """Return the next birthday of contact. If the birthday is on February 29 and today's year is not a leap year,
        move it to March 1.

        :param today: Today's date (date, mandatory)
        :return: Next birthday date (date, optional)
        """
        if self.__birthday is None:
            return None

        birthday: datetime.date = self.__birthday.birthday(today.year)
        if birthday < today:
            birthday = self.__birthday.birthday(today.year + 1)

        return birthday

    def find_phone(self, phone: str) -> Phone:
        """ Search and return the phone number, or raise the phone number not found exception

        :param phone: phone number (string, mandatory)
        :return: phone field, if found (Phone)
        """
        phone_object: Optional[Phone] = self.__find_phone(phone)
        if phone_object is None:
            raise ContactPhoneNotFound()
        return phone_object

    def add_phone(self, phone: str) -> None:
        """ Add the phone number, or raise the phone number already exists exception

        :param phone: phone number (string, mandatory)
        """
        if self.__find_phone(phone):
            raise ContactPhoneAlreadyExist()
        self.__phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """ Remove the phone number, or raise the phone number not found exception

        :param phone: phone number (string, mandatory)
        """
        self.__phones.remove(self.find_phone(phone))

    def edit_phone(self, existing_phone: str, phone: str) -> None:
        """ Edit the phone number, or raise the phone number not found exception

        :param existing_phone: phone number (string, mandatory)
        :param phone: new phone number (string, mandatory)
        """
        self.__phones[self.__phones.index(self.find_phone(existing_phone))] = Phone(phone)

    def find_email(self, email: str) -> Email:
        """ Search and return the email, or raise the email not found exception

        :param email: email (string, mandatory)
        :return: email field, if found (Email)
        """
        email_object: Optional[Email] = self.__find_email(email)
        if email_object is None:
            raise ContactEmailNotFound()
        return email_object

    def add_email(self, email: str) -> None:
        """ Add the email, or raise the email already exists exception

        :param email: email (string, mandatory)
        """
        if self.__find_email(email):
            raise ContactEmailAlreadyExist()
        self.__emails.append(Email(email))

    def remove_email(self, email: str) -> None:
        """ Remove the email, or raise the email not found exception

        :param email: email (string, mandatory)
        """
        self.__emails.remove(self.find_email(email))

    def edit_email(self, existing_email: str, email: str) -> None:
        """ Edit the email, or raise the email not found exception

        :param existing_email: email (string, mandatory)
        :param email: new email (string, mandatory)
        """
        self.__emails[self.__emails.index(self.find_email(existing_email))] = Email(email)
