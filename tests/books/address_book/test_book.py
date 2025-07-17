import unittest
import datetime
from books.address_book.book import AddressBook
from books.address_book.record.record import Record
from books.address_book.error.exceptions import ContactNotFound, ContactAlreadyExist


class TestAddressBook(unittest.TestCase):
    def setUp(self):
        # Create test records
        self.record1 = Record(
            name="John Doe",
            address="123 Main St",
            birthday="01.01.1990",
            phones=["+1234567890"],
            emails=["john@example.com"]
        )
        self.record2 = Record(
            name="Jane Smith",
            address="456 Oak Ave",
            birthday="15.06.1985",
            phones=["+0987654321"],
            emails=["jane@example.com"]
        )
        self.record3 = Record(
            name="Bob Johnson",
            address="789 Pine Rd",
            birthday="30.12.1995",
            phones=["+1122334455"],
            emails=["bob@example.com"]
        )
        
        # Create address book with records
        self.address_book = AddressBook(self.record1, self.record2)

    def test_init(self):
        # Test initialization with records
        self.assertEqual(len(self.address_book), 2)
        self.assertIn("John Doe", self.address_book)
        self.assertIn("Jane Smith", self.address_book)
        
        # Test initialization with duplicate records (should only add unique ones)
        address_book = AddressBook(self.record1, self.record1, self.record2)
        self.assertEqual(len(address_book), 2)
        
        # Test initialization with no records
        empty_book = AddressBook()
        self.assertEqual(len(empty_book), 0)
        
        # Test initialization with custom upcoming_birthdays_period
        custom_period_book = AddressBook(upcoming_birthdays_period=14)
        self.assertEqual(custom_period_book._AddressBook__upcoming_birthdays_period, 14)

    def test_find(self):
        # Test finding existing contact
        record = self.address_book.find("John Doe")
        self.assertEqual(record.name, "John Doe")
        
        # Test finding non-existent contact
        with self.assertRaises(ContactNotFound):
            self.address_book.find("Nonexistent Person")

    def test_add_record(self):
        # Test adding new record
        self.address_book.add_record(self.record3)
        self.assertEqual(len(self.address_book), 3)
        self.assertIn("Bob Johnson", self.address_book)
        
        # Test adding duplicate record
        with self.assertRaises(ContactAlreadyExist):
            self.address_book.add_record(self.record1)

    def test_delete_record(self):
        # Test deleting existing record
        self.address_book.delete_record("John Doe")
        self.assertEqual(len(self.address_book), 1)
        self.assertNotIn("John Doe", self.address_book)
        
        # Test deleting non-existent record
        with self.assertRaises(ContactNotFound):
            self.address_book.delete_record("Nonexistent Person")

    def test_upcoming_birthdays(self):
        # Create a record with birthday today
        today = datetime.datetime.today().date()
        today_str = today.strftime("%d.%m.%Y")
        record_today = Record(name="Today Birthday", birthday=today_str)
        
        # Create a record with birthday tomorrow
        tomorrow = today + datetime.timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%d.%m.%Y")
        record_tomorrow = Record(name="Tomorrow Birthday", birthday=tomorrow_str)
        
        # Create a record with birthday in 10 days (outside default period)
        future = today + datetime.timedelta(days=10)
        future_str = future.strftime("%d.%m.%Y")
        record_future = Record(name="Future Birthday", birthday=future_str)
        
        # Add records to a new address book
        test_book = AddressBook(record_today, record_tomorrow, record_future)
        
        # Test default period (7 days)
        upcoming = list(test_book.upcoming_birthdays())
        self.assertEqual(len(upcoming), 2)  # Should include today and tomorrow
        
        # Test custom period (10 days)
        upcoming = list(test_book.upcoming_birthdays(upcoming_birthdays_period=10))
        self.assertEqual(len(upcoming), 3)  # Should include all three
        
        # Test weekend handling
        # Find a Saturday or Sunday in the next 30 days
        weekend_date = None
        weekend_record = None
        for i in range(1, 30):
            test_date = today + datetime.timedelta(days=i)
            if test_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
                weekend_date = test_date
                weekend_str = weekend_date.strftime("%d.%m.%Y")
                weekend_record = Record(name="Weekend Birthday", birthday=weekend_str)
                break
        
        if weekend_record:
            test_book.add_record(weekend_record)
            upcoming = list(test_book.upcoming_birthdays(upcoming_birthdays_period=30))
            
            # Find the weekend birthday in the results
            weekend_result = next((item for item in upcoming if item[0].name == "Weekend Birthday"), None)
            
            # The congratulation date should be the following Monday
            if weekend_result:
                congratulation_date = weekend_result[1]
                self.assertEqual(congratulation_date.weekday(), 0)  # 0 = Monday
                self.assertTrue(congratulation_date > weekend_date)  # Should be after the actual birthday

    def test_upcoming_birthdays_by_days(self):
        # Create records with birthdays on different days
        today = datetime.datetime.today().date()
        
        # Create two records with birthdays today
        today_str = today.strftime("%d.%m.%Y")
        record_today1 = Record(name="Today Birthday 1", birthday=today_str)
        record_today2 = Record(name="Today Birthday 2", birthday=today_str)
        
        # Create a record with birthday tomorrow
        tomorrow = today + datetime.timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%d.%m.%Y")
        record_tomorrow = Record(name="Tomorrow Birthday", birthday=tomorrow_str)
        
        # Add records to a new address book
        test_book = AddressBook(record_today1, record_today2, record_tomorrow)
        
        # Test grouping by days
        upcoming_by_days = test_book.upcoming_birthdays_by_days()
        
        # Should have 2 days
        self.assertEqual(len(upcoming_by_days), 2)
        
        # Today should have 2 records
        self.assertEqual(len(upcoming_by_days[today]), 2)
        
        # Tomorrow should have 1 record
        self.assertEqual(len(upcoming_by_days[tomorrow]), 1)

    def test_search_by_address(self):
        # Test search by address
        results = self.address_book.search_by_address("Main")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "John Doe")
        
        # Test search with no matches
        results = self.address_book.search_by_address("Nonexistent")
        self.assertEqual(len(results), 0)
        
        # Test search with empty keyword
        results = self.address_book.search_by_address("")
        self.assertEqual(len(results), 0)

    def test_search_by_phone(self):
        # Test search by phone
        results = self.address_book.search_by_phone("1234")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "John Doe")
        
        # Test search with no matches
        results = self.address_book.search_by_phone("9999")
        self.assertEqual(len(results), 0)
        
        # Test search with empty keyword
        results = self.address_book.search_by_phone("")
        self.assertEqual(len(results), 0)

    def test_search_by_email(self):
        # Test search by email
        results = self.address_book.search_by_email("john")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "John Doe")
        
        # Test search with no matches
        results = self.address_book.search_by_email("nonexistent")
        self.assertEqual(len(results), 0)
        
        # Test search with empty keyword
        results = self.address_book.search_by_email("")
        self.assertEqual(len(results), 0)

    def test_search(self):
        # Test search across all fields
        results = self.address_book.search("John")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "John Doe")
        
        # Test search with multiple matches
        results = self.address_book.search("example.com")
        self.assertEqual(len(results), 2)  # Both records have example.com in email
        
        # Test search with no matches
        results = self.address_book.search("nonexistent")
        self.assertEqual(len(results), 0)
        
        # Test search with empty keyword
        results = self.address_book.search("")
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()