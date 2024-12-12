from enum import Enum
from datetime import datetime

class Weekday(Enum):
    """Weekday Enum.

    Follows `datetime.isoweekday()`'s numbering (Monday is 1, Sunday is 7)."""
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

class Condition(Enum):
    """Weather conditions Enum"""
    CLEAR_DAY = 1
    CLEAR_NIGHT = 2
    PARTLY_CLOUDY_DAY = 3
    PARTLY_CLOUDY_NIGHT = 4
    CLOUDY = 5
    RAINY = 6
    STORMY = 7
    SNOWY = 8
    UNKNOWN = -1

class TimeInterval(Enum):
    """Time interval Enum

    Numerical value is in seconds."""
    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800

class WeatherData():
    def __init__(self, condition, date, temp=20, location="SDF"):
        self.condition = condition
        self.date = date
        self.temp = temp
        self.location = location
        self.weekday = Weekday(self.date.isoweekday())
        return

class StockData():
    def __init__(self, ticker, time_series):
        self.ticker = ticker
        self.time_series = time_series
        return
