#!/usr/bin/env python
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock

import waybackpack


class Test(unittest.TestCase):
    def test_basic(self):
        url = "https://www.dol.gov/"
        snapshots = waybackpack.search(url, to_date=1996)
        timestamps = [snap["timestamp"] for snap in snapshots]
        pack = waybackpack.Pack(url, timestamps)
        dirpath = tempfile.mkdtemp()
        pack.download_to(dirpath)
        shutil.rmtree(dirpath)

    def test_no_clobber(self):
        url = "https://whitehouse.gov/"
        snapshots = waybackpack.search(url, to_date=20010510, from_date=20010501)
        timestamps = [snap["timestamp"] for snap in snapshots]
        pack = waybackpack.Pack(url, timestamps)
        dirpath = tempfile.mkdtemp()
        pack.download_to(dirpath, no_clobber=True)
        pack = waybackpack.Pack(url, timestamps)
        for asset in pack.assets:
            asset.fetch = MagicMock(return_value=b"asdfasdf")
        pack.download_to(dirpath, no_clobber=True, delay=1)
        self.assertTrue(
            sum(asset.fetch.call_count for asset in pack.assets) < len(pack.assets)
        )
        shutil.rmtree(dirpath)


if __name__ == "__main__":
    unittest.main()
