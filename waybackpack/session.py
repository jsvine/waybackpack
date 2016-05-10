from .settings import DEFAULT_USER_AGENT
import requests
import time
import logging
logger = logging.getLogger(__name__)

class Session(object):
    def __init__(self, follow_redirects=False, user_agent=DEFAULT_USER_AGENT):
        self.follow_redirects = follow_redirects
        self.user_agent = user_agent

    def get(self, url, **kwargs):
        headers = { "User-Agent": self.user_agent }
        response_is_final = False
        while (response_is_final == False):
            res = requests.get(
                url,
                allow_redirects=self.follow_redirects,
                headers=headers,
                **kwargs
            )
            if res.status_code != 200:
                logger.info("HTTP status code: {0}".format(res.status_code))
            if int(res.status_code / 100) == 5:
                logger.info("Waiting 1 second before retrying.")
                time.sleep(1)
                continue
            else:
                response_is_final = True
        return res
