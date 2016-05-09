from .session import Session
from .settings import DEFAULT_ROOT
import datetime as dt
import re
import time
import sys, os
import logging
logger = logging.getLogger(__name__)

ARCHIVE_TEMPLATE = "https://web.archive.org/web/{timestamp}{flag}/{url}"

REMOVAL_PATTERNS = [
    re.compile(b"<!-- BEGIN WAYBACK TOOLBAR INSERT -->.*?<!-- END WAYBACK TOOLBAR INSERT -->", re.DOTALL),
    re.compile(b'<script type="text/javascript" src="/static/js/analytics.js"></script>'),
    re.compile(b'<script type="text/javascript">archive_analytics.values.server_name=[^<]+</script>'),
    re.compile(b'<link type="text/css" rel="stylesheet" href="/static/css/banner-styles.css"/>'),
]

REDIRECT_PATTERNS = [
    re.compile(b'<p [^>]+>Got an HTTP (30\d) response at crawl time</p>'),
    re.compile(b'<title>\s*Internet Archive Wayback Machine\s*</title>'),
    re.compile(b'<a href="([^"]+)">Impatient\?</a>')
]

class Asset(object):
    def __init__(self, original_url, timestamp):
        self.timestamp = timestamp
        self.original_url = original_url

    def get_archive_url(self, raw=False):
        flag = "id_" if raw else ""
        return ARCHIVE_TEMPLATE.format(
            timestamp=self.timestamp,
            url=self.original_url,
            flag=flag,
        )

    def fetch(self,
            session=None,
            raw=False,
            root=DEFAULT_ROOT):

        session = session or Session()
        url = self.get_archive_url(raw)
        res = session.get(url)
        content = res.content

        if raw:
            return content
        else:
            rdp = REDIRECT_PATTERNS

            is_js_redirect = sum(re.search(pat, content) != None
                for pat in rdp) == len(rdp)

            if is_js_redirect:
                code = re.search(rdp[0], content).group(1).decode("utf-8")
                loc = DEFAULT_ROOT + re.search(rdp[2], content).group(1).decode("utf-8")
                log_msg = "Encountered {0} redirect to {1}."
                logger.info(log_msg.format(code, loc))
                if session.follow_redirects:
                    content = session.get(loc).content
                else:
                    pass

            if re.search(REMOVAL_PATTERNS[0], content) != None:
                for pat in REMOVAL_PATTERNS:
                    content = re.sub(pat, b"", content)
                if root != "":
                    root_pat = re.compile(('([\'"])(/web/' + self.timestamp + ')').encode("utf-8"))
                    content = re.sub(root_pat, (r"\1" + root + r"\2").encode("utf-8"), content)
            return content
