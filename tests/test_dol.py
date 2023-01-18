#!/usr/bin/env python
import unittest

import waybackpack


class Test(unittest.TestCase):
    def test_basic(self):
        url = "http://www.dol.gov/"
        snapshots = waybackpack.search(url)
        timestamps = [snap["timestamp"] for snap in snapshots]
        first = waybackpack.Asset(url, timestamps[0])
        session = waybackpack.Session(follow_redirects=True)
        content = first.fetch(session=session)
        assert b"Regulatory Information" in content
        assert len(content) > 0
