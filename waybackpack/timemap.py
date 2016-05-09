from .session import Session
from .asset import Asset
import re
import time
import datetime
import sys, os
import logging
logger = logging.getLogger(__name__)

MEMENTO_TEMPLATE = "https://web.archive.org/web/timemap/link/{url}"
MEMENTO_TIMESTAMP_PAT = re.compile(r"^<http://web.archive.org/web/(\d+)/")

class TimestampList(list):
    def between(self, start=None, end=None):
        if start != None and not isinstance(start, (str, int)):
            raise ValueError("`start` should be a string or integer.")
        if end != None and not isinstance(end, (str, int)):
            raise ValueError("`end` should be a string or integer.")

        def test_timestamp(t):
            return (
                ((t >= str(start)) or start == None) and
                ((t < str(end)) or end == None)
            )

        return self.__class__(filter(test_timestamp, self))

    def soonest_after(self, timestamp):
        after = self.between(start=timestamp)
        if len(after) > 0:
            return after[0]
        else:
            return None

class TimeMap(object):
    def __init__(self, url):
        self.url = url
        self._timestamps = None

    def get_timestamps(self, session=None):
        if self._timestamps != None: return self._timestamps
        session = session or Session()
        url = MEMENTO_TEMPLATE.format(url=self.url)
        memento = session.get(url).content.decode("utf-8")
        lines = memento.split("\n")
        matches_gen = (re.search(MEMENTO_TIMESTAMP_PAT, line) for line in lines)
        matches = filter(None, matches_gen)
        timestamps = TimestampList(m.group(1) for m in matches)
        self._timestamps = timestamps
        return self._timestamps
