# -*- coding: utf-8 -*-

"""
Tests for address book Record class
"""

import pytest
import datetime
from books.address_book.record.record import Record
from books.address_book.error.exceptions import (
    ContactNameMandatory,
    ContactPhoneNotFound,
    ContactPhoneAlreadyExist,
    ContactEmailNotFound,
    ContactEmailAlreadyExist,
    ContactBirthdayAlreadyExist,
    ContactAddressAlreadyExist,
)


class TestRecord:
    """Tests for the Record class"""

    def test_record_initialization_minimal(self, sample_name):
        """Test Record initialization with minimal parameters"""
        record = Record(sample_name)
        assert record.name == sample_name
        assert record.address == ''  # Returns empty string, not None
        assert record.birthday is None
        assert record.phones == []
        assert record.emails == []
        assert str(record)  # Check that __str__ doesn't raise exceptions

    def test_record_initialization_full(self, sample_name, sample_address, sample_birthday, sample_phone, sample_email):
        """Test Record initialization with all parameters"""
        record = Record(
            sample_name,
            address=sample_address,
            birthday=sample_birthday,
            phones=[sample_phone],
            emails=[sample_email]
        )
        assert record.name == sample_name
        assert record.address == sample_address
        assert str(record.birthday) == sample_birthday
        assert sample_phone in record.phones
        assert sample_email in record.emails
        assert str(record)  # Check that __str__ doesn't raise exceptions

    def test_record_empty_name(self):
        """Test Record with empty name"""
        with pytest.raises(ContactNameMandatory):
            Record("")

    def test_edit_name(self, sample_name):
        """Test editing the name"""
        record = Record(sample_name)
        new_name = "Jane Doe"
        record.edit_name(new_name)
        assert record.name == new_name

    def test_address_operations(self, sample_name, sample_address):
        """Test address operations"""
        record = Record(sample_name)
        
        # Add address
        record.add_address(sample_address)
        assert record.address == sample_address
        
        # Try to add address again
        with pytest.raises(ContactAddressAlreadyExist):
            record.add_address(sample_address)
        
        # Edit address
        new_address = "456 New St, New City, New Country"
        record.edit_address(new_address)
        assert record.address == new_address
        
        # Delete address
        record.delete_address()
        assert record.address == ''  # Returns empty string, not None
        
        # Delete non-existent address (should not raise)
        record.delete_address()
        assert record.address == ''  # Returns empty string, not None

    def test_birthday_operations(self, sample_name, sample_birthday):
        """Test birthday operations"""
        record = Record(sample_name)
        
        # Add birthday
        record.add_birthday(sample_birthday)
        assert str(record.birthday) == sample_birthday
        
        # Try to add birthday again
        with pytest.raises(ContactBirthdayAlreadyExist):
            record.add_birthday(sample_birthday)
        
        # Edit birthday
        new_birthday = "02.02.1992"
        record.edit_birthday(new_birthday)
        assert str(record.birthday) == new_birthday
        
        # Delete birthday
        record.delete_birthday()
        assert record.birthday is None
        
        # Delete non-existent birthday (should not raise)
        record.delete_birthday()
        assert record.birthday is None

    def test_next_birthday(self, sample_name, today):
        """Test next birthday calculation"""
        record = Record(sample_name)
        
        # Set birthday to today
        today_str = today.strftime("%d.%m.1990")
        record.add_birthday(today_str)
        
        # Next birthday should be today (since birthday is today)
        assert record.next_birthday(today) == today
        
        # Set birthday to tomorrow
        tomorrow = today + datetime.timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%d.%m.1990")
        record.edit_birthday(tomorrow_str)
        
        # Next birthday should be tomorrow this year
        expected_tomorrow = tomorrow.replace(year=today.year)
        assert record.next_birthday(today) == expected_tomorrow
        
        # Set birthday to yesterday
        yesterday = today - datetime.timedelta(days=1)
        yesterday_str = yesterday.strftime("%d.%m.1990")
        record.edit_birthday(yesterday_str)
        
        # Next birthday should be next year on that date
        expected_next_year = yesterday.replace(year=today.year + 1)
        assert record.next_birthday(today) == expected_next_year
        
        # Test with no birthday
        record.delete_birthday()
        assert record.next_birthday(today) is None

    def test_phone_operations(self, sample_name, sample_phone):
        """Test phone operations"""
        record = Record(sample_name)
        
        # Add phone
        record.add_phone(sample_phone)
        assert sample_phone in record.phones
        
        # Try to add the same phone again
        with pytest.raises(ContactPhoneAlreadyExist):
            record.add_phone(sample_phone)
        
        # Find phone
        found_phone = record.find_phone(sample_phone)
        assert str(found_phone) == sample_phone
        
        # Find non-existent phone
        with pytest.raises(ContactPhoneNotFound):
            record.find_phone("+9876543210")
        
        # Edit phone
        new_phone = "+9876543210"
        record.edit_phone(sample_phone, new_phone)
        assert new_phone in record.phones
        assert sample_phone not in record.phones
        
        # Edit non-existent phone
        with pytest.raises(ContactPhoneNotFound):
            record.edit_phone(sample_phone, new_phone)
        
        # Remove phone
        record.remove_phone(new_phone)
        assert new_phone not in record.phones
        
        # Remove non-existent phone
        with pytest.raises(ContactPhoneNotFound):
            record.remove_phone(new_phone)

    def test_email_operations(self, sample_name, sample_email):
        """Test email operations"""
        record = Record(sample_name)
        
        # Add email
        record.add_email(sample_email)
        assert sample_email in record.emails
        
        # Try to add the same email again
        with pytest.raises(ContactEmailAlreadyExist):
            record.add_email(sample_email)
        
        # Find email
        found_email = record.find_email(sample_email)
        assert str(found_email) == sample_email
        
        # Find non-existent email
        with pytest.raises(ContactEmailNotFound):
            record.find_email("new.email@example.com")
        
        # Edit email
        new_email = "new.email@example.com"
        record.edit_email(sample_email, new_email)
        assert new_email in record.emails
        assert sample_email not in record.emails
        
        # Edit non-existent email
        with pytest.raises(ContactEmailNotFound):
            record.edit_email(sample_email, new_email)
        
        # Remove email
        record.remove_email(new_email)
        assert new_email not in record.emails
        
        # Remove non-existent email
        with pytest.raises(ContactEmailNotFound):
            record.remove_email(new_email)

    def test_multiple_phones_and_emails(self, sample_name):
        """Test adding multiple phones and emails"""
        record = Record(sample_name)
        
        # Add multiple phones
        phones = ["+15551234567", "+15552345678", "+15553456789"]
        for phone in phones:
            record.add_phone(phone)
        
        assert all(phone in record.phones for phone in phones)
        
        # Add multiple emails
        emails = ["email1@example.com", "email2@example.com", "email3@example.com"]
        for email in emails:
            record.add_email(email)
        
        assert all(email in record.emails for email in emails)