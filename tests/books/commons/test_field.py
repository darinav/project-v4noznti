import unittest
from books.commons.field import Field


class TestField(unittest.TestCase):
    def test_init(self):
        # Test initialization with different types of values
        field1 = Field("test")
        self.assertEqual(field1.value, "test")
        
        field2 = Field(123)
        self.assertEqual(field2.value, 123)
        
        field3 = Field(True)
        self.assertEqual(field3.value, True)
        
        field4 = Field(None)
        self.assertIsNone(field4.value)

    def test_str(self):
        # Test string representation
        field1 = Field("test")
        self.assertEqual(str(field1), "test")
        
        field2 = Field(123)
        self.assertEqual(str(field2), "123")
        
        field3 = Field(None)
        self.assertEqual(str(field3), "None")

    def test_immutability(self):
        # Test that the field is immutable
        field = Field("test")
        with self.assertRaises(AttributeError):
            field.value = "new value"
        
        with self.assertRaises(AttributeError):
            field.new_attr = "something"

    def test_hash(self):
        # Test hash functionality
        field1 = Field("test")
        field2 = Field("test")
        field3 = Field("other")
        
        # Same value should have same hash
        self.assertEqual(hash(field1), hash(field2))
        
        # Different values should have different hashes
        self.assertNotEqual(hash(field1), hash(field3))
        
        # Test in a set
        field_set = {field1, field2, field3}
        self.assertEqual(len(field_set), 2)  # field1 and field2 should be considered the same

    def test_equality(self):
        # Test equality comparison
        field1 = Field("test")
        field2 = Field("test")
        field3 = Field("other")
        
        self.assertEqual(field1, field2)
        self.assertNotEqual(field1, field3)
        self.assertNotEqual(field1, "test")  # Different types


if __name__ == "__main__":
    unittest.main()