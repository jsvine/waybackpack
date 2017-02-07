#!/usr/bin/env python
import unittest
import waybackpack
import sys, os

class Test(unittest.TestCase):
    def test_basic(self):
        url = "dol.gov"
        snapshots = waybackpack.search(url)
        first = waybackpack.Asset(snapshots[0])
        content = first.fetch()
        assert(b"Regulatory Information" in content)        
        assert(len(content) > 0)
