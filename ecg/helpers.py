"""
Signal processing utilities.
"""

from typing import List


def count_zero_crossings(samples: List) -> int:
    """
    Count the number of zero crossings in the provided list of samples.

    :param samples: A list of integers.
    :return: The number of zero crossings in the list.
    """
    count = 0
    for i in range(1, len(samples)):
        # Check if the product is negative -- this implies that one is positive and the other is negative
        if samples[i - 1] * samples[i] < 0:
            count += 1
    return count
