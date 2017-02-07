#!/usr/bin/env python
import unittest
import waybackpack
import sys, os

SNAPSHOT = {'timestamp' : "20160106120201",
            'original' : "https://berniesanders.com/"}

class Test(unittest.TestCase):
    def test_no_redirect(self):
        asset = waybackpack.Asset(SNAPSHOT)
        content = asset.fetch()
        assert(b"Impatient" in content)

    def test_yes_redirect(self):
        session = waybackpack.Session(follow_redirects=True)
        asset = waybackpack.Asset(SNAPSHOT)
        content = asset.fetch(session=session)
        assert(b"Impatient" not in content)
        assert(b"Nobody who works 40 hours" in content)
