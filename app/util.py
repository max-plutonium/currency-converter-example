import poetry_version

from datetime import timedelta
from pytimeparse.timeparse import timeparse


def parse_timeout(value: str, default: str = '30 secs') -> timedelta:
    return timedelta(timeparse(value or default))


def get_app_version():
    return poetry_version.extract(source_file=__file__)
