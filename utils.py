import datetime
from dataclasses import dataclass


def convert_to_datetime(date_from_message: str) -> datetime.datetime:
    pass


@dataclass
class Time:
    hour: int = None
    minute: int = None
