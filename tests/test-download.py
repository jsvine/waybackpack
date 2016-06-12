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
        pack = waybackpack.Pack(url, snapshots=snapshots)
        dirpath = tempfile.mkdtemp()
        pack.download_to(dirpath)
        shutil.rmtree(dirpath)
