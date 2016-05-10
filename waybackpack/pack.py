from .settings import DEFAULT_ROOT
from .session import Session
from .asset import Asset
from .cdx import search
import hashlib
import sys, os
import logging
logger = logging.getLogger(__name__)

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

class Pack(object):
    def __init__(self,
        url,
        timestamps=None,
        uniques_only=False,
        session=None):

        self.url = url
        prefix = "http://" if urlparse(url).scheme == "" else  ""
        self.full_url = prefix + url
        self.parsed_url = urlparse(self.full_url)

        self.session = session or Session()

        self.timestamps = timestamps or [ snap["timestamp"] for snap in search(
            url,
            uniques_only=uniques_only,
            session=self.session
        ) ]
        self.assets = [ Asset(self.url, ts) for ts in self.timestamps ]

    def download_to(self, directory,
        raw=False,
        root=DEFAULT_ROOT):

        for asset in self.assets:
            path_head, path_tail = os.path.split(self.parsed_url.path)
            if path_tail == "":
                path_tail = "index.html"

            filedir = os.path.join(
                directory,
                asset.timestamp,
                self.parsed_url.netloc,
                path_head
            )

            filepath = os.path.join(filedir, path_tail)

            logger.info(
                "Fetching {0} @ {1}".format(
                    asset.original_url, 
                    asset.timestamp)
            )

            content = asset.fetch(
                session=self.session,
                raw=raw,
                root=root
            )

            try:
                os.makedirs(filedir)
            except OSError:
                pass
            with open(filepath, "wb") as f:
                logger.info("Writing to {0}\n".format(filepath))
                f.write(content)
