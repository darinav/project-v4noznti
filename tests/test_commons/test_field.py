# -*- coding: utf-8 -*-

"""
Tests for Field class
"""

import pytest
from books.commons.field import Field


def test_field_initialization():
    """Test Field initialization with different value types"""
    # Test with string
    field_str = Field("test")
    assert field_str.value == "test"
    assert str(field_str) == "test"
    
    # Test with integer
    field_int = Field(123)
    assert field_int.value == 123
    assert str(field_int) == "123"
    
    # Test with None
    field_none = Field(None)
    assert field_none.value is None
    assert str(field_none) == "None"


def test_field_immutability():
    """Test that Field is immutable"""
    field = Field("test")
    
    # Attempt to change the value directly should raise AttributeError
    with pytest.raises(AttributeError):
        field.value = "new value"
    
    # Attempt to add a new attribute should raise AttributeError
    with pytest.raises(AttributeError):
        field.new_attr = "new attribute"


def test_field_equality():
    """Test Field equality comparison"""
    field1 = Field("test")
    field2 = Field("test")
    field3 = Field("different")
    
    # Same value should be equal
    assert field1 == field2
    
    # Different values should not be equal
    assert field1 != field3
    
    # Different types should not be equal
    assert field1 != "test"


def test_field_hash():
    """Test Field hash for use in dictionaries and sets"""
    field1 = Field("test")
    field2 = Field("test")
    field3 = Field("different")
    
    # Create a set of fields
    field_set = {field1, field2, field3}
    
    # Set should deduplicate equal fields
    assert len(field_set) == 2
    
    # Create a dictionary with fields as keys
    field_dict = {field1: "value1", field3: "value3"}
    
    # Should be able to retrieve values using equal fields
    assert field_dict[field2] == "value1"