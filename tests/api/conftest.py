"""
Pytest fixtures for API tests
"""

import pytest

from init import clean_and_initialize


@pytest.fixture(autouse=True)
def cleanup():
    """
    Reinitialize the database before each test run to ensure consistency between tests.
    """
    clean_and_initialize()
    yield
