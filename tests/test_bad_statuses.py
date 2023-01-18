#!/usr/bin/env python
import unittest

import waybackpack

# https://github.com/jsvine/waybackpack/issues/36


class Test(unittest.TestCase):
    def test_503(self):
        asset = waybackpack.Asset(
            "https://www.amazon.com/Art-Gathering-How-Meet-Matters/dp/1594634920",
            timestamp="20190506092829",
        )

        content = asset.fetch()
        assert content is None
