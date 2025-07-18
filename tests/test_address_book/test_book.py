# -*- coding: utf-8 -*-

"""
Tests for AddressBook class
"""

import pytest
import datetime
from books.address_book.book import AddressBook
from books.address_book.record import Record
from books.address_book.error.exceptions import ContactNotFound, ContactAlreadyExist


class TestAddressBook:
    """Tests for the AddressBook class"""

    @pytest.fixture
    def empty_book(self):
        """Return an empty address book"""
        return AddressBook()

    @pytest.fixture
    def sample_record(self, sample_name, sample_address, sample_birthday, sample_phone, sample_email):
        """Return a sample record"""
        return Record(
            sample_name,
            address=sample_address,
            birthday=sample_birthday,
            phones=[sample_phone],
            emails=[sample_email]
        )

    @pytest.fixture
    def populated_book(self, sample_record):
        """Return an address book with a sample record"""
        book = AddressBook()
        book.add_record(sample_record)
        return book

    def test_initialization(self):
        """Test AddressBook initialization"""
        # Default initialization
        book = AddressBook()
        assert len(book) == 0
        assert book._AddressBook__upcoming_birthdays_period == 7  # Default value

        # Custom upcoming_birthdays_period
        book = AddressBook(upcoming_birthdays_period=14)
        assert book._AddressBook__upcoming_birthdays_period == 14

        # Initialize with records
        record1 = Record("John Doe")
        record2 = Record("Jane Doe")
        book = AddressBook(record1, record2)
        assert len(book) == 2
        assert "John Doe" in book
        assert "Jane Doe" in book

    def test_add_record(self, empty_book, sample_record):
        """Test adding a record"""
        # Add a record
        empty_book.add_record(sample_record)
        assert sample_record.name in empty_book
        assert empty_book[sample_record.name] == sample_record

        # Try to add the same record again
        with pytest.raises(ContactAlreadyExist):
            empty_book.add_record(sample_record)

    def test_find(self, populated_book, sample_record):
        """Test finding a record"""
        # Find existing record
        found_record = populated_book.find(sample_record.name)
        assert found_record == sample_record

        # Find non-existent record
        with pytest.raises(ContactNotFound):
            populated_book.find("Non-existent Name")

    def test_delete_record(self, populated_book, sample_record):
        """Test deleting a record"""
        # Delete existing record
        populated_book.delete_record(sample_record.name)
        assert sample_record.name not in populated_book

        # Delete non-existent record
        with pytest.raises(ContactNotFound):
            populated_book.delete_record(sample_record.name)

    def test_iteration(self, empty_book, sample_name):
        """Test iterating through records"""
        # Add multiple records
        records = [Record(f"{sample_name} {i}") for i in range(5)]
        for record in records:
            empty_book.add_record(record)

        # Iterate through records
        iterated_records = list(empty_book)
        assert len(iterated_records) == 5
        for record in records:
            assert record.name in iterated_records

    def test_upcoming_birthdays(self, empty_book, today):
        """Test upcoming birthdays calculation"""
        # Create records with birthdays on different days
        today_str = today.strftime("%d.%m.1990")
        tomorrow = today + datetime.timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%d.%m.1990")
        next_week = today + datetime.timedelta(days=7)
        next_week_str = next_week.strftime("%d.%m.1990")
        next_month = today + datetime.timedelta(days=30)
        next_month_str = next_month.strftime("%d.%m.1990")

        # Add records with different birthdays
        record1 = Record("Person Today", birthday=today_str)
        record2 = Record("Person Tomorrow", birthday=tomorrow_str)
        record3 = Record("Person Next Week", birthday=next_week_str)
        record4 = Record("Person Next Month", birthday=next_month_str)
        record5 = Record("Person No Birthday")

        empty_book.add_record(record1)
        empty_book.add_record(record2)
        empty_book.add_record(record3)
        empty_book.add_record(record4)
        empty_book.add_record(record5)

        # Test with default period (7 days)
        upcoming = list(empty_book.upcoming_birthdays())
        assert len(upcoming) == 3  # Today, tomorrow, and next week
        assert any(str(record.contact.name) == "Person Today" for record in upcoming)
        assert any(str(record.contact.name) == "Person Tomorrow" for record in upcoming)
        assert any(str(record.contact.name) == "Person Next Week" for record in upcoming)
        assert not any(str(record.contact.name) == "Person Next Month" for record in upcoming)
        assert not any(str(record.contact.name) == "Person No Birthday" for record in upcoming)

        # Test with custom period (30 days)
        upcoming = list(empty_book.upcoming_birthdays(30))
        assert len(upcoming) == 4  # Today, tomorrow, next week, and next month
        assert any(str(record.contact.name) == "Person Today" for record in upcoming)
        assert any(str(record.contact.name) == "Person Tomorrow" for record in upcoming)
        assert any(str(record.contact.name) == "Person Next Week" for record in upcoming)
        assert any(str(record.contact.name) == "Person Next Month" for record in upcoming)
        assert not any(str(record.contact.name) == "Person No Birthday" for record in upcoming)

    def test_upcoming_birthdays_by_days(self, empty_book, today):
        """Test upcoming birthdays by days calculation"""
        # Create records with birthdays on different days
        today_str = today.strftime("%d.%m.1990")
        tomorrow = today + datetime.timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%d.%m.1990")
        next_week = today + datetime.timedelta(days=7)
        next_week_str = next_week.strftime("%d.%m.1990")

        # Add records with different birthdays
        record1 = Record("Person Today 1", birthday=today_str)
        record2 = Record("Person Today 2", birthday=today_str)
        record3 = Record("Person Tomorrow", birthday=tomorrow_str)
        record4 = Record("Person Next Week", birthday=next_week_str)

        empty_book.add_record(record1)
        empty_book.add_record(record2)
        empty_book.add_record(record3)
        empty_book.add_record(record4)

        # Test with default period (7 days)
        upcoming_by_days = empty_book.upcoming_birthdays_by_days()
        
        # Should have 3 days with birthdays
        assert len(upcoming_by_days) == 3
        
        # Today should have 2 people
        today_date = today
        assert today_date in upcoming_by_days
        assert len(upcoming_by_days[today_date]) == 2
        
        # Tomorrow should have 1 person (but shifted to Monday since tomorrow is Saturday)
        monday_date = tomorrow + datetime.timedelta(days=2)  # Saturday + 2 days = Monday
        assert monday_date in upcoming_by_days
        assert len(upcoming_by_days[monday_date]) == 1
        
        # Next week should have 1 person
        next_week_date = next_week
        assert next_week_date in upcoming_by_days
        assert len(upcoming_by_days[next_week_date]) == 1

    def test_search_by_address(self, empty_book):
        """Test searching by address"""
        # Create records with different addresses
        record1 = Record("Person 1", address="123 Main St, City")
        record2 = Record("Person 2", address="456 Main St, City")
        record3 = Record("Person 3", address="789 Side St, Town")
        record4 = Record("Person 4")  # No address

        empty_book.add_record(record1)
        empty_book.add_record(record2)
        empty_book.add_record(record3)
        empty_book.add_record(record4)

        # Search for "Main"
        results = empty_book.search_by_address("Main")
        assert len(results) == 2
        assert any(str(record.name) == "Person 1" for record in results)
        assert any(str(record.name) == "Person 2" for record in results)

        # Search for "City"
        results = empty_book.search_by_address("City")
        assert len(results) == 2
        assert any(str(record.name) == "Person 1" for record in results)
        assert any(str(record.name) == "Person 2" for record in results)

        # Search for "Town"
        results = empty_book.search_by_address("Town")
        assert len(results) == 1
        assert str(results[0].name) == "Person 3"

        # Search for non-existent address
        results = empty_book.search_by_address("Non-existent")
        assert len(results) == 0

    def test_search_by_phone(self, empty_book):
        """Test searching by phone"""
        # Create records with different phones
        record1 = Record("Person 1", phones=["+15551234567"])
        record2 = Record("Person 2", phones=["+15552345678"])
        record3 = Record("Person 3", phones=["+15553456789", "+15554567890"])
        record4 = Record("Person 4")  # No phones

        empty_book.add_record(record1)
        empty_book.add_record(record2)
        empty_book.add_record(record3)
        empty_book.add_record(record4)

        # Search for specific phone
        results = empty_book.search_by_phone("+15551234567")
        assert len(results) == 1
        assert str(results[0].name) == "Person 1"

        # Search for partial phone
        results = empty_book.search_by_phone("345")
        assert len(results) == 3  # All three contain "345"
        assert any(str(record.name) == "Person 1" for record in results)
        assert any(str(record.name) == "Person 2" for record in results)
        assert any(str(record.name) == "Person 3" for record in results)

        # Search for non-existent phone
        results = empty_book.search_by_phone("999")
        assert len(results) == 0

    def test_search_by_email(self, empty_book):
        """Test searching by email"""
        # Create records with different emails
        record1 = Record("Person 1", emails=["john@example.com"])
        record2 = Record("Person 2", emails=["jane@example.com"])
        record3 = Record("Person 3", emails=["john@company.com", "john.doe@gmail.com"])
        record4 = Record("Person 4")  # No emails

        empty_book.add_record(record1)
        empty_book.add_record(record2)
        empty_book.add_record(record3)
        empty_book.add_record(record4)

        # Search for specific email
        results = empty_book.search_by_email("john@example.com")
        assert len(results) == 1
        assert str(results[0].name) == "Person 1"

        # Search for partial email
        results = empty_book.search_by_email("john")
        assert len(results) == 2
        assert any(str(record.name) == "Person 1" for record in results)
        assert any(str(record.name) == "Person 3" for record in results)

        # Search for domain
        results = empty_book.search_by_email("example.com")
        assert len(results) == 2
        assert any(str(record.name) == "Person 1" for record in results)
        assert any(str(record.name) == "Person 2" for record in results)

        # Search for non-existent email
        results = empty_book.search_by_email("nonexistent")
        assert len(results) == 0

    def test_search(self, empty_book):
        """Test general search"""
        # Create records with different attributes
        record1 = Record("John Doe", address="123 Main St", phones=["+15551234567"], emails=["john@example.com"])
        record2 = Record("Jane Smith", address="456 Side St", phones=["+15552345678"], emails=["jane@example.com"])
        record3 = Record("John Smith", address="789 Back St", phones=["+15553456789"], emails=["john@company.com"])

        empty_book.add_record(record1)
        empty_book.add_record(record2)
        empty_book.add_record(record3)

        # Search for name
        results = empty_book.search("John")
        assert len(results) == 2
        assert any(str(record.name) == "John Doe" for record in results)
        assert any(str(record.name) == "John Smith" for record in results)

        # Search for address
        results = empty_book.search("Main")
        assert len(results) == 1
        assert str(results[0].name) == "John Doe"

        # Search for phone
        results = empty_book.search("234")
        assert len(results) == 2
        assert any(str(record.name) == "John Doe" for record in results)
        assert any(str(record.name) == "Jane Smith" for record in results)

        # Search for email
        results = empty_book.search("example.com")
        assert len(results) == 2
        assert any(str(record.name) == "John Doe" for record in results)
        assert any(str(record.name) == "Jane Smith" for record in results)

        # Search for non-existent term
        results = empty_book.search("nonexistent")
        assert len(results) == 0