#!/usr/bin/env python
import unittest
import waybackpack
import sys, os

class Test(unittest.TestCase):
    def test_snapshot_index(self):
        url = "dol.gov"
        snapshots = waybackpack.search(url)
        assert(len(snapshots) > 0)
        assert(snapshots[0]["timestamp"] == "19961102145216")
        clipped = waybackpack.search(
            url,
            to_date="1996"
        )
        assert(len(clipped) < len(snapshots))
        assert(len(clipped) == 4)

    def test_uniques(self):
        url = "dol.gov"
        uniques = waybackpack.search(
            url,
            to_date="1996",
            uniques_only=True
        )
        assert(len(uniques) == 2)

