#!/usr/bin/env python
import unittest
import waybackpack
import sys, os

class Test(unittest.TestCase):
    def test_snapshot_index(self):
        tm = waybackpack.TimeMap("dol.gov")
        ts = tm.get_timestamps()
        assert(len(ts) > 0)
        assert(ts[0] == "19961102145216")
        clipped = ts.between("1996", "1997")
        assert(len(clipped) < len(ts))
        assert(len(clipped) == 4)
