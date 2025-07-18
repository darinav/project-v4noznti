# -*- coding: utf-8 -*-

"""
Shared fixtures for tests
"""

import pytest
from datetime import datetime, date

# Common fixtures that might be used across multiple test files

@pytest.fixture
def today():
    """Return a fixed date for testing"""
    return date(2025, 7, 18)  # Using the current date from the issue description

@pytest.fixture
def sample_name():
    """Return a sample name for testing"""
    return "John Doe"

@pytest.fixture
def sample_phone():
    """Return a sample phone number for testing"""
    return "+15551234567"

@pytest.fixture
def sample_email():
    """Return a sample email for testing"""
    return "john.doe@example.com"

@pytest.fixture
def sample_birthday():
    """Return a sample birthday for testing"""
    return "01.01.1990"

@pytest.fixture
def sample_address():
    """Return a sample address for testing"""
    return "123 Main St, City, Country"

@pytest.fixture
def sample_title():
    """Return a sample note title for testing"""
    return "Sample Note"

@pytest.fixture
def sample_text():
    """Return a sample note text for testing"""
    return "This is a sample note text."

@pytest.fixture
def sample_tags():
    """Return sample tags for testing"""
    return ["tag1", "tag2", "tag3"]