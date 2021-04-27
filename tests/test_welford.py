import math

import pytest

from stats.welford import update, calculate_stats


def test_one_value():
    count = 0
    mean = 0.0
    m2 = 0.0

    new_value = 42
    count, mean, m2 = update(count, mean, m2, new_value)
    assert count == 1
    assert mean == new_value

    stats = calculate_stats(count, mean, m2)
    assert stats['count'] == 1
    assert stats['mean'] == new_value
    assert stats['sd'] == 0


def test_two_values():
    count = 0
    mean = 0.0
    m2 = 0.0

    new_value = 42
    count, mean, m2 = update(count, mean, m2, new_value)
    assert count == 1
    assert mean == new_value

    new_value = 44
    count, mean, m2 = update(count, mean, m2, new_value)
    assert count == 2
    assert mean == 43

    stats = calculate_stats(count, mean, m2)
    assert stats['count'] == 2
    assert stats['mean'] == 43
    assert stats['sd'] == 1


def test_more_values():
    count = 0
    mean = 0.0
    m2 = 0.0

    numbers = (10000000004.0, 10000000007.0, 10000000013.0, 10000000016.0)
    for new_value in numbers:
        count, mean, m2 = update(count, mean, m2, new_value)

    stats = calculate_stats(count, mean, m2)
    assert stats['count'] == len(numbers)
    assert stats['mean'] == 10000000010
    assert math.isclose(stats['sd'], 4.7434164902526)


def test_invalid_input():
    with pytest.raises(ValueError):
        calculate_stats(0, 42, 43)
