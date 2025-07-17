import unittest
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Discover and run all tests
if __name__ == "__main__":
    # Create a test suite
    test_suite = unittest.TestSuite()

    # Manually add all test modules
    # Commons tests
    from tests.books.commons.test_field import TestField

    # Address Book tests
    from tests.books.address_book.record.test_fields import TestName, TestBirthday, TestPhone, TestEmail, TestAddress
    from tests.books.address_book.record.test_record import TestRecord
    from tests.books.address_book.test_book import TestAddressBook

    # Note Book tests
    from tests.books.note_book.note.test_fields import TestTitle, TestText, TestTag, TestTags
    from tests.books.note_book.note.test_note import TestNote
    from tests.books.note_book.test_book import TestNoteBook

    # Add all test classes to the suite
    test_loader = unittest.TestLoader()
    test_suite.addTests([
        test_loader.loadTestsFromTestCase(TestField),
        test_loader.loadTestsFromTestCase(TestName),
        test_loader.loadTestsFromTestCase(TestBirthday),
        test_loader.loadTestsFromTestCase(TestPhone),
        test_loader.loadTestsFromTestCase(TestEmail),
        test_loader.loadTestsFromTestCase(TestAddress),
        test_loader.loadTestsFromTestCase(TestRecord),
        test_loader.loadTestsFromTestCase(TestAddressBook),
        test_loader.loadTestsFromTestCase(TestTitle),
        test_loader.loadTestsFromTestCase(TestText),
        test_loader.loadTestsFromTestCase(TestTag),
        test_loader.loadTestsFromTestCase(TestTags),
        test_loader.loadTestsFromTestCase(TestNote),
        test_loader.loadTestsFromTestCase(TestNoteBook),
    ])

    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)

    # Exit with non-zero code if tests failed
    sys.exit(not result.wasSuccessful())
