"""
An implementation of Welford's online algorithm.
See https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Welford%27s_online_algorithm
"""
import math


def update(count: int, mean: float, m2: float, new_value: float) -> tuple:
    """
    For a new value and current tracking data, compute the new
    tracking data which can be passed to calculate_stats if needed.

    :param count: number of data points so far
    :param mean: mean of all data points so far
    :param m2: aggregate of the squared distance from the mean so far
    :param new_value: new_value to take account of

    :returns: (count, mean, m2) after taking into account new_value
    """
    count += 1
    delta = new_value - mean
    mean += delta / count

    delta2 = new_value - mean
    m2 += delta * delta2

    return count, mean, m2


def calculate_stats(count: int, mean: float, m2: float) -> dict:
    """
    Return current stats in a dictionary, including calculating
    the standard deviation.

    :param count: number of data points so far
    :param mean: mean of all data points so far
    :param m2: aggregate of the squared distance from the mean so far

    :returns: A dict with entries count, mean & sd (standard deviation)

    :raises ValueError: if count is less than 1
    """
    if count < 1:
        raise ValueError()
    else:
        sd = math.sqrt(m2 / count)
        return dict(count=count, mean=mean, sd=sd)
