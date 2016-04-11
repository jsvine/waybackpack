import logging
logger = logging.getLogger(__name__)

# Python 2/3 compatibility
try:
    import urllib.request as rq
    from urllib.parse import urlparse
except ImportError:
    import urllib2 as rq
    from urlparse import urlparse

# Don't follow redirects
class NoRedirectHandler(rq.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        log_msg = "Encountered {0} redirect to {1}; not following it."
        logger.info(log_msg.format(code, headers.get("Location")))
        return fp
    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302

urlopen = rq.build_opener(NoRedirectHandler()).open
