import unittest
import datetime
from books.address_book.record.record import Name, Birthday, Phone, Email, Address
from books.address_book.error.exceptions import (
    ContactNameMandatory,
    ContactPhoneValueError,
    ContactEmailValueError,
    ContactBirthdayValueError,
    ContactAddressCannotBeEmpty,
)


class TestName(unittest.TestCase):
    def test_valid_name(self):
        # Test valid name
        name = Name("John Doe")
        self.assertEqual(str(name), "John Doe")
        
        name = Name("A")  # Single character should be valid
        self.assertEqual(str(name), "A")

    def test_invalid_name(self):
        # Test empty name
        with self.assertRaises(ContactNameMandatory):
            Name("")
        
        # Test None name
        with self.assertRaises(ContactNameMandatory):
            Name(None)


class TestBirthday(unittest.TestCase):
    def test_valid_birthday(self):
        # Test valid birthday
        birthday = Birthday("01.01.2000")
        self.assertEqual(str(birthday), "01.01.2000")
        self.assertEqual(birthday.date_of_birth(), datetime.date(2000, 1, 1))
        
        # Test leap year
        birthday = Birthday("29.02.2000")
        self.assertEqual(str(birthday), "29.02.2000")
        self.assertEqual(birthday.date_of_birth(), datetime.date(2000, 2, 29))

    def test_invalid_birthday(self):
        # Test invalid format
        with self.assertRaises(ContactBirthdayValueError):
            Birthday("2000-01-01")  # Wrong format
        
        # Test invalid date
        with self.assertRaises(ContactBirthdayValueError):
            Birthday("30.02.2000")  # February doesn't have 30 days
        
        with self.assertRaises(ContactBirthdayValueError):
            Birthday("31.04.2000")  # April doesn't have 31 days

    def test_birthday_method(self):
        # Test birthday method with leap year
        birthday = Birthday("29.02.2000")
        
        # Test with leap year
        self.assertEqual(birthday.birthday(2020), datetime.date(2020, 2, 29))
        
        # Test with non-leap year (should move to March 1)
        self.assertEqual(birthday.birthday(2021), datetime.date(2021, 3, 1))
        
        # Test with regular date
        birthday = Birthday("15.06.2000")
        self.assertEqual(birthday.birthday(2021), datetime.date(2021, 6, 15))


class TestPhone(unittest.TestCase):
    def test_valid_phone(self):
        # Test valid phone numbers
        phone = Phone("+1234567890")
        self.assertEqual(str(phone), "+1234567890")
        
        # Test with formatting
        phone = Phone("+1 (234) 567-890")
        self.assertEqual(str(phone), "+1234567890")
        
        # Test without + (should add it)
        phone = Phone("1234567890")
        self.assertEqual(str(phone), "+1234567890")

    def test_invalid_phone(self):
        # Test empty phone
        with self.assertRaises(ContactPhoneValueError):
            Phone("")
        
        # Test None phone
        with self.assertRaises(ContactPhoneValueError):
            Phone(None)
        
        # Test invalid phone format
        with self.assertRaises(ContactPhoneValueError):
            Phone("abc")


class TestEmail(unittest.TestCase):
    def test_valid_email(self):
        # Test valid emails
        email = Email("test@example.com")
        self.assertEqual(str(email), "test@example.com")
        
        # Test with whitespace (should be removed)
        email = Email("test @example.com")
        self.assertEqual(str(email), "test@example.com")
        
        # Test with different domains
        email = Email("test@sub.example.co.uk")
        self.assertEqual(str(email), "test@sub.example.co.uk")

    def test_invalid_email(self):
        # Test empty email
        with self.assertRaises(ContactEmailValueError):
            Email("")
        
        # Test None email
        with self.assertRaises(ContactEmailValueError):
            Email(None)
        
        # Test invalid email format
        with self.assertRaises(ContactEmailValueError):
            Email("test@")
        
        with self.assertRaises(ContactEmailValueError):
            Email("test@example")
        
        with self.assertRaises(ContactEmailValueError):
            Email("test.example.com")


class TestAddress(unittest.TestCase):
    def test_valid_address(self):
        # Test valid address
        address = Address("123 Main St, City, Country")
        self.assertEqual(str(address), "123 Main St, City, Country")
        
        # Test minimal address
        address = Address("A")  # Single character should be valid
        self.assertEqual(str(address), "A")

    def test_invalid_address(self):
        # Test empty address
        with self.assertRaises(ContactAddressCannotBeEmpty):
            Address("")
        
        # Test None address
        with self.assertRaises(ContactAddressCannotBeEmpty):
            Address(None)


if __name__ == "__main__":
    unittest.main()