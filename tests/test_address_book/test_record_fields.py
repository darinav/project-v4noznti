# -*- coding: utf-8 -*-

"""
Tests for address book record field classes
"""

import pytest
import datetime
from books.address_book.record.record import Name, Birthday, Phone, Email, Address
from books.address_book.error.exceptions import (
    ContactNameMandatory,
    ContactBirthdayValueError,
    ContactPhoneValueError,
    ContactEmailValueError,
    ContactAddressCannotBeEmpty,
)


class TestName:
    """Tests for the Name class"""

    def test_name_initialization(self, sample_name):
        """Test Name initialization"""
        name = Name(sample_name)
        assert name.value == sample_name
        assert str(name) == sample_name

    def test_name_empty_string(self):
        """Test Name with empty string"""
        with pytest.raises(ContactNameMandatory):
            Name("")


class TestBirthday:
    """Tests for the Birthday class"""

    def test_birthday_initialization(self, sample_birthday):
        """Test Birthday initialization with valid date"""
        birthday = Birthday(sample_birthday)
        assert isinstance(birthday.value, datetime.date)
        assert str(birthday) == sample_birthday

    def test_birthday_invalid_format(self):
        """Test Birthday with invalid format"""
        with pytest.raises(ContactBirthdayValueError):
            Birthday("01/01/1990")  # Wrong format, should be DD.MM.YYYY

    def test_birthday_invalid_date(self):
        """Test Birthday with invalid date"""
        with pytest.raises(ContactBirthdayValueError):
            Birthday("30.02.1990")  # Invalid date (February 30)

    def test_birthday_future_date(self):
        """Test Birthday with future date"""
        future_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d.%m.%Y")
        # Birthday class doesn't validate for future dates, so this should work
        birthday = Birthday(future_date)
        assert isinstance(birthday.value, datetime.date)

    def test_date_of_birth(self):
        """Test date_of_birth property"""
        birthday = Birthday("01.01.1990")
        assert birthday.date_of_birth() == datetime.date(1990, 1, 1)

    def test_birthday_calculation(self):
        """Test birthday calculation for a specific year"""
        birthday = Birthday("01.01.1990")
        # Test for a non-leap year
        assert birthday.birthday(2023) == datetime.date(2023, 1, 1)
        # Test for a leap year
        assert birthday.birthday(2024) == datetime.date(2024, 1, 1)

    def test_february_29_birthday(self):
        """Test birthday calculation for February 29"""
        birthday = Birthday("29.02.2000")  # Leap year
        # In non-leap years, should return March 1 (implementation behavior)
        assert birthday.birthday(2023) == datetime.date(2023, 3, 1)
        # In leap years, should return February 29
        assert birthday.birthday(2024) == datetime.date(2024, 2, 29)


class TestPhone:
    """Tests for the Phone class"""

    def test_phone_initialization(self, sample_phone):
        """Test Phone initialization with valid phone number"""
        phone = Phone(sample_phone)
        assert phone.value == sample_phone
        assert str(phone) == sample_phone

    def test_phone_normalization(self):
        """Test Phone number normalization"""
        # Test with spaces and dashes
        phone = Phone("+1 234-567-8901")
        assert phone.value == "+12345678901"

        # Test with parentheses
        phone = Phone("+1 (234) 567-8901")
        assert phone.value == "+12345678901"

    def test_phone_invalid_format(self):
        """Test Phone with invalid format"""
        with pytest.raises(ContactPhoneValueError):
            Phone("not a phone number")

        with pytest.raises(ContactPhoneValueError):
            Phone("12345")  # Too short

        with pytest.raises(ContactPhoneValueError):
            Phone("1234567890")  # Missing country code


class TestEmail:
    """Tests for the Email class"""

    def test_email_initialization(self, sample_email):
        """Test Email initialization with valid email"""
        email = Email(sample_email)
        assert email.value == sample_email
        assert str(email) == sample_email

    def test_email_normalization(self):
        """Test Email normalization"""
        # Test with uppercase - implementation doesn't normalize case
        email = Email("John.Doe@Example.com")
        assert email.value == "John.Doe@Example.com"

    def test_email_invalid_format(self):
        """Test Email with invalid format"""
        with pytest.raises(ContactEmailValueError):
            Email("not an email")

        with pytest.raises(ContactEmailValueError):
            Email("user@")  # Missing domain

        with pytest.raises(ContactEmailValueError):
            Email("@example.com")  # Missing username


class TestAddress:
    """Tests for the Address class"""

    def test_address_initialization(self, sample_address):
        """Test Address initialization"""
        address = Address(sample_address)
        assert address.value == sample_address
        assert str(address) == sample_address

    def test_address_empty_string(self):
        """Test Address with empty string"""
        with pytest.raises(ContactAddressCannotBeEmpty):
            Address("")

    def test_address_whitespace_only(self):
        """Test Address with whitespace only"""
        # Implementation doesn't validate whitespace-only strings
        address = Address("   ")
        assert address.value == "   "
        assert str(address) == "   "