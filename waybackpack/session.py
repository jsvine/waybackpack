from .settings import DEFAULT_USER_AGENT
import requests
import time
import logging
logger = logging.getLogger(__name__)

class Session(object):
    def __init__(self,
        follow_redirects=False,
        user_agent=DEFAULT_USER_AGENT,
        max_retries=3,
    ):
        self.follow_redirects = follow_redirects
        self.user_agent = user_agent
        self.max_retries = max_retries

    def get(self, url, **kwargs):
        headers = {
            "User-Agent": self.user_agent,
        }
        response_is_final = False
        retries = 0
        while (response_is_final == False):
            res = requests.get(
                url,
                allow_redirects=self.follow_redirects,
                headers=headers,
                stream=True,
                **kwargs
            )

            if res.status_code != 200:
                logger.info("HTTP status code: {0}".format(res.status_code))

            if int(res.status_code / 100) in [ 4, 5 ]: # 4XX and 5XX codes
                logger.info("Waiting 1 second before retrying.")
                retries += 1
                if retries <= self.max_retries:
                    logger.info("Waiting 1 second before retrying.")
                    time.sleep(1)
                    continue
                else:
                    logger.info("Maximum retries reached, skipping.")
                    return None
            else:
                response_is_final = True
        return res
