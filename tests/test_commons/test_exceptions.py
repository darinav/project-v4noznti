# -*- coding: utf-8 -*-

"""
Tests for common exceptions
"""

import pytest
from books.commons.exceptions import ObjectNotFound, ObjectAlreadyExist, ObjectValueError


def test_object_not_found_exception():
    """Test ObjectNotFound exception"""
    # Test with a custom message
    message = "Test object not found"
    exception = ObjectNotFound(message)
    
    # Check that the exception is a subclass of KeyError
    assert isinstance(exception, KeyError)
    
    # Check that the message is preserved
    assert str(exception) == f"'{message}'"
    
    # Test raising the exception
    with pytest.raises(ObjectNotFound) as excinfo:
        raise ObjectNotFound(message)
    
    assert str(excinfo.value) == f"'{message}'"


def test_object_already_exist_exception():
    """Test ObjectAlreadyExist exception"""
    # Test with a custom message
    message = "Test object already exists"
    exception = ObjectAlreadyExist(message)
    
    # Check that the exception is a subclass of KeyError
    assert isinstance(exception, KeyError)
    
    # Check that the message is preserved
    assert str(exception) == f"'{message}'"
    
    # Test raising the exception
    with pytest.raises(ObjectAlreadyExist) as excinfo:
        raise ObjectAlreadyExist(message)
    
    assert str(excinfo.value) == f"'{message}'"


def test_object_value_error_exception():
    """Test ObjectValueError exception"""
    # Test with a custom message
    message = "Test object value error"
    exception = ObjectValueError(message)
    
    # Check that the exception is a subclass of ValueError
    assert isinstance(exception, ValueError)
    
    # Check that the message is preserved
    assert str(exception) == message
    
    # Test raising the exception
    with pytest.raises(ObjectValueError) as excinfo:
        raise ObjectValueError(message)
    
    assert str(excinfo.value) == message


def test_exception_inheritance():
    """Test exception inheritance"""
    # ObjectNotFound should be caught by KeyError
    with pytest.raises(KeyError):
        raise ObjectNotFound("Test")
    
    # ObjectAlreadyExist should be caught by KeyError
    with pytest.raises(KeyError):
        raise ObjectAlreadyExist("Test")
    
    # ObjectValueError should be caught by ValueError
    with pytest.raises(ValueError):
        raise ObjectValueError("Test")