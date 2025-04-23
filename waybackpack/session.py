import logging
import time

import requests

from .settings import DEFAULT_USER_AGENT

logger = logging.getLogger(__name__)


class Session(object):
    def __init__(
        self,
        follow_redirects=False,
        user_agent=DEFAULT_USER_AGENT,
        max_retries=3,
        delay_retry=5,
        proxy=None,
        verify=True
    ):
        self.follow_redirects = follow_redirects
        self.user_agent = user_agent
        self.max_retries = max_retries
        self.delay_retry = delay_retry
        self.proxy = proxy
        self.verify = verify

    def try_get(self, url, **kwargs):
        headers = {
            "User-Agent": self.user_agent,
        }
        try:
            res = requests.get(
                url,
                allow_redirects=self.follow_redirects,
                headers=headers,
                stream=True,
                proxies={'http': self.proxy, 'https': self.proxy} if self.proxy else None,
                verify=self.verify,
                **kwargs
            )

            if int(res.status_code / 100) in [4, 5]:  # 4XX and 5XX codes
                return False, res
            else:
                return True, res

        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
        ):
            logger.info("Connection error")
            return False, None

    def get(self, url, **kwargs):
        retries = 0
        while True:
            success, res = self.try_get(url, **kwargs)
            if success:
                if res.status_code != 200:
                    logger.info("HTTP status code: {0}".format(res.status_code))
                return res
            else:
                logger.info(
                    "Waiting {0} second(s) before retrying.".format(self.delay_retry)
                )
                time.sleep(self.delay_retry)
                retries += 1
                if retries <= self.max_retries:
                    continue
                else:
                    logger.info("Maximum retries reached, skipping.")
                    return None
