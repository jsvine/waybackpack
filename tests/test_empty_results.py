#!/usr/bin/env python
import unittest

import waybackpack

# via https://github.com/jsvine/waybackpack/issues/39

URL = "https://indianexpress.com/section/lifestyle/health/feed/"


class Test(unittest.TestCase):
    def test_empty_result(self):
        timestamps = waybackpack.search(URL, from_date="2080")

        assert len(timestamps) == 0

        pack = waybackpack.Pack(
            URL,
            timestamps=timestamps,
        )
        assert len(pack.timestamps) == 0
