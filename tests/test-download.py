#!/usr/bin/env python
import unittest
import waybackpack
import sys, os
import shutil
import tempfile

class Test(unittest.TestCase):
    def test_basic(self):
        url = "dol.gov"
        timemap = waybackpack.TimeMap(url)
        timestamps = timemap.get_timestamps().between(None, 1997)
        pack = waybackpack.Pack(url, timestamps)
        dirpath = tempfile.mkdtemp()
        pack.download_to(dirpath)
        shutil.rmtree(dirpath)
