#!/usr/bin/env python
import unittest
import waybackpack
import sys, os
import shutil
import tempfile

class Test(unittest.TestCase):
    def test_basic(self):
        url = "dol.gov"
        snapshots = waybackpack.search(url, to_date=1996)
        timestamps = [ snap["timestamp"] for snap in snapshots ]
        pack = waybackpack.Pack(url, timestamps)
        dirpath = tempfile.mkdtemp()
        pack.download_to(dirpath)
        shutil.rmtree(dirpath)
