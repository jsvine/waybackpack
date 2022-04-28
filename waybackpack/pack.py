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

try:
    from tqdm.auto import tqdm
    has_tqdm = True
except: 
    has_tqdm = False

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

        if timestamps is None:
            self.timestamps = [ snap["timestamp"] for snap in search(
                url,
                uniques_only=uniques_only,
                session=self.session
            ) ]
        else:
            self.timestamps = timestamps

        self.assets = [ Asset(self.url, ts) for ts in self.timestamps ]

    def download_to(self, directory,
        raw=False,
        root=DEFAULT_ROOT,
        ignore_errors=False,
        no_clobber=False,
        progress=False):

        if progress and not has_tqdm:
            raise Exception("To print progress bars, you must have `tqdm` installed. To install: pip install tqdm.")

        for asset in (tqdm(self.assets) if progress else self.assets) :
            path_head, path_tail = os.path.split(self.parsed_url.path)
            if path_tail == "":
                path_tail = "index.html"

            filedir = os.path.join(
                directory,
                asset.timestamp,
                self.parsed_url.netloc,
                path_head.lstrip("/")
            )

            filepath = os.path.join(filedir, path_tail)

            if no_clobber and (os.path.exists(filepath) and os.path.getsize(filepath) > 0):
                continue

            logger.info(
                "Fetching {0} @ {1}".format(
                    asset.original_url, 
                    asset.timestamp)
            )

            try:
                content = asset.fetch(
                    session=self.session,
                    raw=raw,
                    root=root
                )

                if content is None:
                    continue

            except Exception as e:
                if ignore_errors == True:
                    ex_name = ".".join([ e.__module__, e.__class__.__name__ ])
                    logger.warn("ERROR -- {0} @ {1} -- {2}: {3}".format(
                        asset.original_url,
                        asset.timestamp,
                        ex_name,
                        e
                    ))
                    continue
                else:
                    raise

            try:
                os.makedirs(filedir)
            except OSError:
                pass

            with open(filepath, "wb") as f:
                logger.info("Writing to {0}\n".format(filepath))
                f.write(content)
