from . import request
import datetime as dt
import re
import time
import sys, os
import logging
logger = logging.getLogger(__name__)

DEFAULT_USER_AGENT = "waybackpack"
DEFAULT_ROOT = "https://web.archive.org"
MEMENTO_TEMPLATE = "https://web.archive.org/web/timemap/link/{url}"
ARCHIVE_TEMPLATE = "https://web.archive.org/web/{timestamp}{flag}/{url}"

MEMENTO_TIMESTAMP_PAT = re.compile(r"^<http://web.archive.org/web/(\d+)/")
class SnapshotView(object):
    removal_patterns = [
        re.compile(b"<!-- BEGIN WAYBACK TOOLBAR INSERT -->.*?<!-- END WAYBACK TOOLBAR INSERT -->", re.DOTALL),
        re.compile(b'<script type="text/javascript" src="/static/js/analytics.js"></script>'),
        re.compile(b'<script type="text/javascript">archive_analytics.values.server_name=[^<]+</script>'),
        re.compile(b'<link type="text/css" rel="stylesheet" href="/static/css/banner-styles.css"/>'),
    ]

    redirect_patterns = [
        re.compile(b'<p [^>]+>Got an HTTP (30\d) response at crawl time</p>'),
        re.compile(b'<title>\s*Internet Archive Wayback Machine\s*</title>'),
        re.compile(b'<a href="([^"]+)">Impatient\?</a>')
    ]

    def __init__(self, snapshot,
            original=False,
            root=DEFAULT_ROOT):
        self.snapshot = snapshot
        self.original = original
        self.root = root

    def fetch(self, user_agent=DEFAULT_USER_AGENT):
        flag = "id_" if self.original else ""
        content = self.snapshot.fetch(flag=flag, user_agent=user_agent)
        if self.original:
            return content
        else:
            rdp = self.redirect_patterns

            is_redirect = sum(re.search(pat, content) != None
                for pat in rdp) == len(rdp)

            if is_redirect:
                code = re.search(rdp[0], content).group(1).decode("utf-8")
                loc = re.search(rdp[2], content).group(1).decode("utf-8")
                log_msg = "Encountered {0} redirect to {1}; not following it."
                logger.info(log_msg.format(code, loc))
                return b""

            elif re.search(self.removal_patterns[0], content) == None:
                return content

            else:
                for pat in self.removal_patterns:
                    content = re.sub(pat, b"", content)
                if self.root != "":
                    ts = self.snapshot.timestamp
                    root_pat = re.compile(('([\'"])(/web/' + ts + ')').encode("utf-8"))
                    content = re.sub(root_pat, (r"\1" + self.root + r"\2").encode("utf-8"), content)
                return content

class Snapshot(object):
    def __init__(self, resource, timestamp):
        self.resource = resource
        self.timestamp = timestamp

    def get_url(self, flag=""):
        return ARCHIVE_TEMPLATE.format(
            timestamp=self.timestamp,
            url=self.resource.url,
            flag=flag,
        )

    @property
    def url_archive(self):
        return self.get_url()

    @property
    def url_original(self):
        return self.get_url("id_")

    def fetch(self, flag="", user_agent=DEFAULT_USER_AGENT):
        url = self.get_url(flag)
        req = request.rq.Request(url, headers={"User-Agent": user_agent})
        content = None
        while content == None:
            try:
                content = request.urlopen(req).read()
                response_is_final = True
            except request.rq.HTTPError as e:
                log_msg = "Encountered {0} error."
                logger.info(log_msg.format(e.code, url))
                # On 5xx errors, sleep one second and try again
                if int(e.code / 100) == 5: 
                    time.sleep(1)
                    continue
                else:
                    content = e.fp.read()
        return content

class Resource(object):
    def __init__(self, url):
        self.url = url

        prefix = "http://" if request.urlparse(url).scheme == "" else  ""
        self.full_url = prefix + url
        self.parsed_url = request.urlparse(self.full_url)
    
    @property
    def timestamps(self):
        if hasattr(self, "_timestamps"): return self._timestamps
        url = MEMENTO_TEMPLATE.format(url=self.url)
        memento = request.urlopen(url).read().decode("utf-8")
        lines = memento.split("\n")
        matches = filter(None, (re.search(MEMENTO_TIMESTAMP_PAT, line) for line in lines))
        _timestamps = [ m.group(1) for m in matches ]
        self._timestamps = _timestamps
        return _timestamps

    @property
    def snapshots(self):
        return [ Snapshot(self, t) for t in self.timestamps ]
    
    def between(self, start=None, end=None):
        if start != None and not isinstance(start, (str, int)):
            raise ValueError("`start` should be a string or integer.")
        if end != None and not isinstance(end, (str, int)):
            raise ValueError("`end` should be a string or integer.")

        new = self.__class__(self.url)
        timestamps = new.timestamps

        def test_timestamp(t):
            return (
                ((t >= str(start)) or start == None) and 
                ((t <= str(end)) or end == None)
            )

        new._timestamps = list(filter(test_timestamp, timestamps))

        return new

    def download_to(self, directory,
        original=False,
        root=DEFAULT_ROOT,
        user_agent=DEFAULT_USER_AGENT,
        prefix=None,
        suffix=None):

        if prefix == None:
            chunk = self.full_url[len(self.parsed_url.scheme)+3:] 
            prefix = re.sub(r"[^a-zA-Z0-9]+", "-", chunk).strip("-") + "-"

        if suffix == None:
            base, ext = os.path.splitext(self.parsed_url.path)
            if ext == "":
                suffix = ".html"
            else:
                suffix = ext

        for snapshot in self.snapshots:
            view = SnapshotView(snapshot,
                original=original,
                root=root)

            ts = snapshot.timestamp
            filename = "{prefix}{ts}{suffix}".format(
                prefix=prefix, ts=ts, suffix=suffix)
            path = os.path.join(directory, filename)

            with open(path, "wb") as f:
                logger.info("Fetching {0}".format(ts))
                content = view.fetch(user_agent=user_agent)

                logger.info("Writing to {0}\n".format(path))
                f.write(content) 
