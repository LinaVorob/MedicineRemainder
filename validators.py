import datetime
import re
from re import Match
from typing import Optional

from config.config import PATTERN, PATTERN_TIME_CLASSIC, PATTERN_TIME_WORDS


def date_format_validator(str_date: str) -> Optional[Match[str]]:
    pattern = PATTERN
    match = re.search(pattern, str_date)
    if match:
        return match


def validator_digit(str_count: str) -> bool:
    return str_count.isdigit() and int(str_count) > 0


def validator_float(str_answer: str) -> bool:
    try:
        res = float(str_answer)
        return True
    except ValueError:
        return False


def validator_time(answer_time: str) -> bool:
    match_classic = re.search(PATTERN_TIME_CLASSIC, answer_time)
    match_words = re.search(PATTERN_TIME_WORDS, answer_time)
    if match_words or match_classic:
        return True
    if validator_digit(answer_time):
        return True
    if validator_float(answer_time):
        return True
    return False
