# Add your common constants here that are common for all other apps.

from enum import IntEnum
from pickle import NONE

class Currency(IntEnum):
    USD = 1
    INR = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class Suggestions(IntEnum):
    NONE = 0
    BUY = 1
    SELL = 2
    HOLD = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]