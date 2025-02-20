import statistics
from functools import wraps
import json


def get_temps_list(func):
    """
    Decorator function that extracts the temperature values from a list of weather data
    and passes them to the decorated function.

    Args:
        func (function): A function that takes a list of temperatures as its argument.

    Returns:
        wrapper (function): A wrapper function that extracts temperatures from weather data
                             and calls the original function.
    """

    @wraps(func)
    def wrapper(weather_data: list):
        temps = [item["temp"] for item in weather_data]
        return func(temps)

    return wrapper


@get_temps_list
def calc_median(temps: list):
    """
    Calculates the median of a list of temperatures.

    Args:
        temps (list): A list of temperature values.

    Returns:
        float: The median temperature value from the list.
    """
    median_temp = statistics.median(temps)
    return median_temp


@get_temps_list
def calc_mean(temps: list):
    """
    Calculates the mean (average) of a list of temperatures.

    Args:
        temps (list): A list of temperature values.

    Returns:
        float: The mean (average) temperature value from the list.
    """
    mean_temp = statistics.mean(temps)
    return mean_temp


@get_temps_list
def calc_min(temps: list):
    """
    Finds the minimum temperature from a list of temperatures.

    Args:
        temps (list): A list of temperature values.

    Returns:
        float: The minimum temperature value from the list.
    """
    min_temp = min(temps)
    return min_temp


@get_temps_list
def calc_max(temps: list):
    """
    Finds the maximum temperature from a list of temperatures.

    Args:
        temps (list): A list of temperature values.

    Returns:
        float: The maximum temperature value from the list.
    """
    max_temp = max(temps)
    return max_temp
