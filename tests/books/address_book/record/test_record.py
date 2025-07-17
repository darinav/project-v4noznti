import unittest
import datetime
from books.address_book.record.record import Record
from books.address_book.error.exceptions import (
    ContactPhoneNotFound,
    ContactPhoneAlreadyExist,
    ContactEmailNotFound,
    ContactEmailAlreadyExist,
    ContactBirthdayAlreadyExist,
    ContactAddressAlreadyExist,
)


class TestRecord(unittest.TestCase):
    def setUp(self):
        # Create a basic record for testing
        self.record = Record(
            name="John Doe",
            address="123 Main St",
            birthday="01.01.2000",
            phones=["+1234567890", "+0987654321"],
            emails=["john@example.com", "doe@example.com"]
        )

    def test_init(self):
        # Test initialization with all parameters
        self.assertEqual(self.record.name, "John Doe")
        self.assertEqual(self.record.address, "123 Main St")
        self.assertEqual(str(self.record.birthday), "01.01.2000")
        self.assertEqual(len(self.record.phones), 2)
        self.assertIn("+1234567890", self.record.phones)
        self.assertIn("+0987654321", self.record.phones)
        self.assertEqual(len(self.record.emails), 2)
        self.assertIn("john@example.com", self.record.emails)
        self.assertIn("doe@example.com", self.record.emails)

        # Test initialization with minimal parameters
        record_minimal = Record(name="Jane Doe")
        self.assertEqual(record_minimal.name, "Jane Doe")
        self.assertEqual(len(record_minimal.phones), 0)
        self.assertEqual(len(record_minimal.emails), 0)
        self.assertIsNone(record_minimal.birthday)

    def test_str(self):
        # Test string representation
        expected = "Contact name: John Doe, birthday: 01.01.2000, phones: +1234567890; +0987654321, emails: john@example.com; doe@example.com, address: 123 Main St"
        self.assertEqual(str(self.record), expected)

        # Test with minimal record
        record_minimal = Record(name="Jane Doe")
        self.assertEqual(str(record_minimal), "Contact name: Jane Doe")

    def test_edit_name(self):
        # Test editing name
        self.record.edit_name("Jane Doe")
        self.assertEqual(self.record.name, "Jane Doe")

    def test_address_methods(self):
        # Test deleting address
        self.record.delete_address()
        self.assertIsNone(self.record.address)  # Should be None after deletion

        # Test adding address
        self.record.add_address("456 New St")
        self.assertEqual(self.record.address, "456 New St")

        # Test adding address when one already exists
        with self.assertRaises(ContactAddressAlreadyExist):
            self.record.add_address("789 Another St")

        # Test editing address
        self.record.edit_address("789 Another St")
        self.assertEqual(self.record.address, "789 Another St")

    def test_birthday_methods(self):
        # Test deleting birthday
        self.record.delete_birthday()
        self.assertIsNone(self.record.birthday)  # Should be None after deletion

        # Test adding birthday
        self.record.add_birthday("15.06.1990")
        self.assertEqual(str(self.record.birthday), "15.06.1990")

        # Test adding birthday when one already exists
        with self.assertRaises(ContactBirthdayAlreadyExist):
            self.record.add_birthday("20.07.1995")

        # Test editing birthday
        self.record.edit_birthday("20.07.1995")
        self.assertEqual(str(self.record.birthday), "20.07.1995")

    def test_next_birthday(self):
        # Test next birthday calculation
        # Set birthday to a specific date
        self.record.edit_birthday("15.06.1990")

        # Test when birthday is in the future this year
        today = datetime.date(2023, 5, 1)  # May 1, 2023
        next_bday = self.record.next_birthday(today)
        self.assertEqual(next_bday, datetime.date(2023, 6, 15))

        # Test when birthday has passed this year
        today = datetime.date(2023, 7, 1)  # July 1, 2023
        next_bday = self.record.next_birthday(today)
        self.assertEqual(next_bday, datetime.date(2024, 6, 15))

        # Test with no birthday
        self.record.delete_birthday()
        self.assertIsNone(self.record.next_birthday(datetime.date.today()))

    def test_phone_methods(self):
        # Test finding phone
        phone = self.record.find_phone("+1234567890")
        self.assertEqual(str(phone), "+1234567890")

        # Test finding non-existent phone
        with self.assertRaises(ContactPhoneNotFound):
            self.record.find_phone("+1111111111")

        # Test adding phone
        self.record.add_phone("+1111111111")
        self.assertIn("+1111111111", self.record.phones)

        # Test adding existing phone
        with self.assertRaises(ContactPhoneAlreadyExist):
            self.record.add_phone("+1234567890")

        # Test editing phone
        self.record.edit_phone("+1234567890", "+2222222222")
        self.assertIn("+2222222222", self.record.phones)
        self.assertNotIn("+1234567890", self.record.phones)

        # Test removing phone
        self.record.remove_phone("+2222222222")
        self.assertNotIn("+2222222222", self.record.phones)

        # Test removing non-existent phone
        with self.assertRaises(ContactPhoneNotFound):
            self.record.remove_phone("+3333333333")

    def test_email_methods(self):
        # Test finding email
        email = self.record.find_email("john@example.com")
        self.assertEqual(str(email), "john@example.com")

        # Test finding non-existent email
        with self.assertRaises(ContactEmailNotFound):
            self.record.find_email("nonexistent@example.com")

        # Test adding email
        self.record.add_email("new@example.com")
        self.assertIn("new@example.com", self.record.emails)

        # Test adding existing email
        with self.assertRaises(ContactEmailAlreadyExist):
            self.record.add_email("john@example.com")

        # Test editing email
        self.record.edit_email("john@example.com", "updated@example.com")
        self.assertIn("updated@example.com", self.record.emails)
        self.assertNotIn("john@example.com", self.record.emails)

        # Test removing email
        self.record.remove_email("updated@example.com")
        self.assertNotIn("updated@example.com", self.record.emails)

        # Test removing non-existent email
        with self.assertRaises(ContactEmailNotFound):
            self.record.remove_email("nonexistent@example.com")


if __name__ == "__main__":
    unittest.main()
