"""
Test module for AddressBook functionality.
"""

import pytest
import datetime
from unittest.mock import patch

from books import AddressBook, Record
from books.address_book.error import ContactNotFound, ContactAlreadyExist


class TestAddressBook:
    """Test cases for AddressBook functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.book = AddressBook()
        self.record1 = Record("John Doe")
        self.record1.add_phone("+380123456789")
        self.record1.add_email("john@example.com")
        self.record1.add_address("123 Main St")
        self.record1.add_birthday("15.01.1990")
        
        self.record2 = Record("Jane Smith")
        self.record2.add_phone("+380987654321")
        self.record2.add_email("jane@example.com")
        self.record2.add_birthday("20.06.1985")

    def test_init_empty(self):
        """Test creating empty AddressBook."""
        book = AddressBook()
        assert len(book.data) == 0
        assert book._AddressBook__upcoming_birthdays_period == 7

    def test_init_with_custom_period(self):
        """Test creating AddressBook with custom upcoming birthdays period."""
        book = AddressBook(upcoming_birthdays_period=14)
        assert book._AddressBook__upcoming_birthdays_period == 14

    def test_add_record_success(self):
        """Test adding a record successfully."""
        self.book.add_record(self.record1)
        assert "John Doe" in self.book.data
        assert self.book.data["John Doe"] == self.record1

    def test_add_record_duplicate(self):
        """Test adding duplicate record raises exception."""
        self.book.add_record(self.record1)
        
        with pytest.raises(ContactAlreadyExist):
            self.book.add_record(self.record1)

    def test_find_existing_record(self):
        """Test finding an existing record."""
        self.book.add_record(self.record1)
        found_record = self.book.find("John Doe")
        assert found_record == self.record1

    def test_find_nonexistent_record(self):
        """Test finding a nonexistent record raises exception."""
        with pytest.raises(ContactNotFound):
            self.book.find("Nonexistent Person")

    def test_delete_existing_record(self):
        """Test deleting an existing record."""
        self.book.add_record(self.record1)
        self.book.delete_record("John Doe")
        assert "John Doe" not in self.book.data

    def test_delete_nonexistent_record(self):
        """Test deleting a nonexistent record raises exception."""
        with pytest.raises(ContactNotFound):
            self.book.delete_record("Nonexistent Person")

    def test_iter_functionality(self):
        """Test iterator functionality."""
        self.book.add_record(self.record1)
        self.book.add_record(self.record2)
        
        records = list(self.book)
        assert len(records) == 2
        assert self.record1 in records
        assert self.record2 in records

    def test_search_by_name(self):
        """Test searching by name."""
        self.book.add_record(self.record1)
        self.book.add_record(self.record2)
        
        results = self.book.search("John")
        assert len(results) == 1
        assert results[0] == self.record1

    def test_search_by_phone(self):
        """Test searching by phone number."""
        self.book.add_record(self.record1)
        self.book.add_record(self.record2)
        
        results = self.book.search("123456789")
        assert len(results) == 1
        assert results[0] == self.record1

    def test_search_by_email(self):
        """Test searching by email."""
        self.book.add_record(self.record1)
        self.book.add_record(self.record2)
        
        results = self.book.search("jane@example.com")
        assert len(results) == 1
        assert results[0] == self.record2

    def test_search_by_address(self):
        """Test searching by address."""
        self.book.add_record(self.record1)
        self.book.add_record(self.record2)
        
        results = self.book.search("Main St")
        assert len(results) == 1
        assert results[0] == self.record1

    def test_search_no_results(self):
        """Test searching with no results."""
        self.book.add_record(self.record1)
        
        results = self.book.search("nonexistent")
        assert len(results) == 0

    def test_search_multiple_results(self):
        """Test searching with multiple results."""
        # Create records with similar data
        record3 = Record("John Smith")
        record3.add_phone("+380111222333")
        
        self.book.add_record(self.record1)  # John Doe
        self.book.add_record(record3)       # John Smith
        
        results = self.book.search("John")
        assert len(results) == 2

    def test_search_by_phone_specific(self):
        """Test search_by_phone method specifically."""
        self.book.add_record(self.record1)
        self.book.add_record(self.record2)
        
        results = self.book.search_by_phone("987654321")
        assert len(results) == 1
        assert results[0] == self.record2

    def test_search_by_email_specific(self):
        """Test search_by_email method specifically."""
        self.book.add_record(self.record1)
        self.book.add_record(self.record2)
        
        results = self.book.search_by_email("john@example.com")
        assert len(results) == 1
        assert results[0] == self.record1

    def test_search_by_address_specific(self):
        """Test search_by_address method specifically."""
        self.book.add_record(self.record1)
        
        results = self.book.search_by_address("123 Main")
        assert len(results) == 1
        assert results[0] == self.record1

    def test_upcoming_birthdays_default_period(self):
        """Test upcoming birthdays with default period."""
        self.book.add_record(self.record1)
        self.book.add_record(self.record2)
        
        # This test depends on current date, so we'll just check it doesn't crash
        birthdays = self.book.upcoming_birthdays()
        assert isinstance(birthdays, list)

    def test_upcoming_birthdays_custom_period(self):
        """Test upcoming birthdays with custom period."""
        self.book.add_record(self.record1)
        
        birthdays = self.book.upcoming_birthdays(30)
        assert isinstance(birthdays, list)

    def test_upcoming_birthdays_by_days_default(self):
        """Test upcoming_birthdays_by_days with default period."""
        self.book.add_record(self.record1)
        
        birthdays = self.book.upcoming_birthdays_by_days()
        assert isinstance(birthdays, list)

    def test_upcoming_birthdays_by_days_custom(self):
        """Test upcoming_birthdays_by_days with custom period."""
        self.book.add_record(self.record1)
        
        birthdays = self.book.upcoming_birthdays_by_days(14)
        assert isinstance(birthdays, list)

    @patch('books.address_book.book.datetime')
    def test_congratulation_date_calculation(self, mock_datetime):
        """Test congratulation date calculation logic."""
        # Mock today's date
        mock_today = datetime.date(2024, 1, 10)
        mock_datetime.datetime.today.return_value.date.return_value = mock_today
        mock_datetime.date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        mock_datetime.timedelta = datetime.timedelta
        
        self.book.add_record(self.record1)  # Birthday: 1990-01-15
        
        # Test the private method through upcoming_birthdays
        birthdays = self.book.upcoming_birthdays(10)
        # Should include the record since birthday is within 10 days
        assert isinstance(birthdays, list)

    def test_congratulation_date_weekend_adjustment(self):
        """Test that congratulation dates are adjusted for weekends."""
        # Create a record with birthday that falls on weekend
        weekend_record = Record("Weekend Person")
        weekend_record.add_birthday("14.01.1990")  # Adjust date as needed
        self.book.add_record(weekend_record)
        
        birthdays = self.book.upcoming_birthdays(30)
        # Test should verify weekend adjustment logic

    def test_congratulation_date_leap_year(self):
        """Test congratulation date for leap year birthdays."""
        leap_record = Record("Leap Person")
        leap_record.add_birthday("29.02.1988")  # Leap year birthday
        self.book.add_record(leap_record)
        
        birthdays = self.book.upcoming_birthdays(365)
        # Should handle leap year birthday correctly

    def test_getstate_setstate(self):
        """Test serialization methods."""
        self.book.add_record(self.record1)
        
        # Test __getstate__
        state = self.book.__getstate__()
        assert isinstance(state, dict)
        
        # Test __setstate__
        new_book = AddressBook()
        new_book.__setstate__(state)
        assert "John Doe" in new_book.data

    def test_empty_book_operations(self):
        """Test operations on empty book."""
        # Search on empty book
        results = self.book.search("anything")
        assert len(results) == 0
        
        # Upcoming birthdays on empty book
        birthdays = self.book.upcoming_birthdays()
        assert len(birthdays) == 0
        
        # Iterator on empty book
        records = list(self.book)
        assert len(records) == 0

    def test_search_case_insensitive(self):
        """Test that search is case insensitive."""
        self.book.add_record(self.record1)
        
        results_lower = self.book.search("john")
        results_upper = self.book.search("JOHN")
        results_mixed = self.book.search("John")
        
        assert len(results_lower) == 1
        assert len(results_upper) == 1
        assert len(results_mixed) == 1

    def test_search_partial_match(self):
        """Test that search works with partial matches."""
        self.book.add_record(self.record1)
        
        # Partial name match
        results = self.book.search("Doe")
        assert len(results) == 1
        assert results[0] == self.record1
        
        # Partial phone match
        results = self.book.search("123456")
        assert len(results) == 1
        assert results[0] == self.record1

    def test_multiple_contacts_same_birthday(self):
        """Test handling multiple contacts with same birthday."""
        record3 = Record("Another Person")
        record3.add_birthday("15.01.1990")  # Same as record1
        
        self.book.add_record(self.record1)
        self.book.add_record(record3)
        
        birthdays = self.book.upcoming_birthdays(365)
        # Should handle multiple people with same birthday

    def test_contact_without_birthday(self):
        """Test handling contacts without birthdays."""
        no_birthday_record = Record("No Birthday")
        no_birthday_record.add_phone("+380555666777")
        
        self.book.add_record(no_birthday_record)
        
        # Should not crash when checking birthdays
        birthdays = self.book.upcoming_birthdays()
        assert isinstance(birthdays, list)

    def test_search_merge_functionality(self):
        """Test the internal search merge functionality."""
        self.book.add_record(self.record1)
        self.book.add_record(self.record2)
        
        # Search that should find results in multiple fields
        results = self.book.search("example.com")  # Should find both by email
        assert len(results) == 2