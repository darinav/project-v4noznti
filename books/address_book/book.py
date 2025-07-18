# -*- coding: utf-8 -*-

"""
Address Book class implementation
"""

import datetime
from typing import Optional
from collections import UserDict, namedtuple, defaultdict
from collections.abc import Iterator


from .error import ContactNotFound, ContactAlreadyExist
from .record import Record


class AddressBook(UserDict):
    def __init__(self, *args, upcoming_birthdays_period: int = 7):
        """ Initialize an Address Book with the specified Contacts and the birthday congratulations days range, if given

        :param args: the contact records (Record, optional)
        :param upcoming_birthdays_period: the default birthday congratulations days range (int)
        """
        super().__init__()
        self.__upcoming_birthdays_period = upcoming_birthdays_period or 7
        # Add contact records if given, removing duplicates
        for contact in args:
            if str(contact.name) not in self:
                self.add_record(contact)

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, value):
        self.__dict__ = value

    def __iter__(self):
        """ Return iterable object for the sorted keys

        :return: sorted keys (iterable object)
        """
        return iter(sorted(self.data))

    def __congratulation_date(
            self,
            contact: Record,
            today: Optional[datetime.date] = None,
            upcoming_birthdays_period: Optional[int] = None,
    ) -> Optional[datetime.date]:
        """Private method for calculation the congratulation date.
        If the birthday is not within the next congratulation_range_days days, including today, return None.
        If the birthday falls on a weekend, the congratulation date is shifted to the following Monday.

        :param today: Today's date, if not specified, is calculated as the current date (date, optional)
        :param upcoming_birthdays_period: the birthday congratulations days range (int, optional)
        :return: Congratulation date (datetime.date, optional)
        """
        try:
            # If today parameter is None, determine the current date
            if today is None:
                today = datetime.datetime.today().date()
            if not upcoming_birthdays_period:
                upcoming_birthdays_period = self.__upcoming_birthdays_period

            # Calculate next birthday
            next_birthday: Optional[datetime.date] = contact.next_birthday(today)

            # Verify if the birthday is within the next congratulation_range_days days, including today
            if next_birthday is None or not 0 <= (next_birthday - today).days <= upcoming_birthdays_period:
                # If the birthday does not exist or is not within the next congratulation_range_days days,
                # including today, return None
                return None

            # Verify if the birthday falls on a weekend
            if next_birthday.isoweekday() in {6, 7, }:
                # Shift the congratulation date to the following Monday, as it falls on a weekend
                next_birthday += datetime.timedelta(days=((7 - next_birthday.isoweekday()) + 1))

            # Return congratulation date as string in 'YYYY.MM.DD' format
            return next_birthday
        except Exception as e:
            # An unexpected error occurred
            # Raise an exception to the upper level
            raise Exception("An unexpected error occurred: {error}.".format(error=repr(e)))

    def find(self, name: str) -> Record:
        """ Search and return the contact record, or raise the contact not found exception

        :param name: contact name (string, mandatory)
        :return: contact record, if found (Record)
        """
        if name not in self:
            # Contact found - raise the contact not found exception
            raise ContactNotFound
        # Return the contact
        return self.get(name, None)

    def add_record(self, contact: Record) -> None:
        """ Add the contact record, or raise the contact already exists exception

        :param contact: contact record (Record, mandatory)
        """
        if str(contact.name) in self:
            # Contact found - raise the contact already exists exception
            raise ContactAlreadyExist()
        # Add the contact record
        self.data[str(contact.name)] = contact

    def delete_record(self, name: str) -> None:
        """ Remove the contact record, or raise the contact not found exception

        :param name: contact name (string, mandatory)
        """
        if name not in self:
            # Contact not found - raise the contact not found exception
            raise ContactNotFound()
        # Remove the contact record
        self.pop(name, None)

    def upcoming_birthdays(
            self,
            upcoming_birthdays_period: Optional[int] = None,
    ) -> Iterator[tuple[Record, datetime.date]]:
        """Return all contacts whose birthday is within the next period, including today,
        along with the congratulation date. If the birthday falls on a weekend, the congratulation date
        is moved to the following Monday.

        :param upcoming_birthdays_period: the birthday congratulations days range (int, optional)
        :return: The next contacts whose birthday is within the next period, including today,
        along with the congratulation date (Iterator of tuple)
        """

        # Named tuple creation
        UpcomingBirthday = namedtuple('UpcomingBirthday', ['contact', 'congratulation_date'])

        today: datetime.date = datetime.datetime.today().date()
        for contact in self.values():
            if (
                    congratulation_date := self.__congratulation_date(
                        contact,
                        today=today,
                        upcoming_birthdays_period=upcoming_birthdays_period,
                    )
            ) is not None:
                # Return the upcoming birthday contact and the congratulation date
                yield UpcomingBirthday(contact, congratulation_date)

    def upcoming_birthdays_by_days(
            self,
            upcoming_birthdays_period: Optional[int] = None,
    ) -> dict[datetime.date, list[Record]]:
        """Return all contacts whose birthday is within the next period, including today, grouped by date,
        along with the congratulation date. If the birthday falls on a weekend, the congratulation date
        is moved to the following Monday.

        :param upcoming_birthdays_period: the birthday congratulations days range (int, optional)
        :return: contacts whose birthday is within the next period, grouped by date (dictionary)
        """

        # Collect contacts whose birthday is within the next period with the congratulation date
        upcoming_birthdays: dict[datetime.date, list[Record]] = defaultdict(list)
        for record, congratulation_date in self.upcoming_birthdays(upcoming_birthdays_period=upcoming_birthdays_period):
            upcoming_birthdays[congratulation_date].append(record)

        # Sort and return contacts birthdays by date
        return dict(sorted(upcoming_birthdays.items()))

    def __search_merge(self, *args) -> list[Record]:
        """ Merge search result sets and return the contact records

        :param args: search result sets (set of string, optional)
        :return: found contact records (list of Records)
        """
        found_keys: set[str] = set()
        # Combine the search results into a single set
        for result in args:
            if isinstance(result, set):
                found_keys.update(result)
        # Return found records
        return [value for key, value in self.items() if key in found_keys]

    def search_by_address(self, keyword: str) -> list[Record]:
        """ Search and return the contact records by keyword/sequence in the address

        :param keyword: search keyword or sequence (string, mandatory)
        :return: found contact records (list of Records)
        """
        return self.__search_merge({key for key, value in self.items() if keyword and keyword in value.address})

    def search_by_phone(self, keyword: str) -> list[Record]:
        """ Search and return the contact records by keyword/sequence in the phone numbers

        :param keyword: search keyword or sequence (string, mandatory)
        :return: found contact records (list of Records)
        """
        return self.__search_merge(
            {key for key, value in self.items() if keyword and [i for i in value.phones if keyword in i]}
        )

    def search_by_email(self, keyword: str) -> list[Record]:
        """ Search and return the contact records by keyword/sequence in the emails

        :param keyword: search keyword or sequence (string, mandatory)
        :return: found contact records (list of Records)
        """
        return self.__search_merge(
            {key for key, value in self.items() if keyword and [i for i in value.emails if keyword in i]}
        )

    def search(self, keyword: str) -> list[Record]:
        """ Search and return the contact records by keyword/sequence in the name, address, phone numbers and emails

        :param keyword: search keyword or sequence (string, mandatory)
        :return: found contact records (list of Records)
        """
        return self.__search_merge(
            {key for key, value in self.items() if keyword and keyword in value.name},
            {key for key, value in self.items() if keyword and keyword in value.address},
            {key for key, value in self.items() if keyword and [i for i in value.phones if keyword in i]},
            {key for key, value in self.items() if keyword and [i for i in value.emails if keyword in i]},
        )
