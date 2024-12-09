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

class WeatherData():
    def __init__(self, condition, date, temp=20, location="SDF"):
        self.condition = condition
        self.date = date
        self.temp = temp
        self.location = location
        self.weekday = Weekday(self.date.isoweekday())
        return
