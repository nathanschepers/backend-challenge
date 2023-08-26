"""
Unit tests for the count_zero_crossings function.
"""
from typing import List

import pytest

from ecg.helpers import count_zero_crossings


@pytest.mark.parametrize(
    "series,expected",
    [
        ([1, 2, 3, -2, -3, 2, 2, -2, 4], 4),
        ([1, 2, 3, 4, 5], 0),
        ([-1, -2, -3, -4], 0),
        ([], 0),
    ],
)
def test_count_zero_crossings(series: List, expected: int) -> None:
    assert count_zero_crossings(series) == expected
