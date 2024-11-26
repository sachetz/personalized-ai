"""
Utils for Gmail Integration
"""

import time
import random
import logging

from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

def robust_request(request_func, max_retries=5):
    """
    Executes a Gmail API request with exponential backoff on failure.
    
    :param request_func: Function that makes the API request
    :param max_retries: Maximum number of retries
    :return: Result of the API request
    """

    for attempt in range(max_retries):
        try:
            return request_func()
        except HttpError as error:
            if error.resp.status in [429, 500, 503]:
                sleep_time = (2 ** attempt) + random.uniform(0, 1)
                logger.warning(
                    "API error %s. Retrying in %s seconds...",
                    str(error.resp.status),
                    f"{sleep_time:.2f}"
                )
                time.sleep(sleep_time)
            elif error.resp.status in [401, 403]:
                logger.error("Authentication error %s: %s", str(error.resp.status), str(error))
                raise error
            else:
                logger.error("Unexpected API error %s: %s", str(error.resp.status), str(error))
                raise error
    logger.error("Max retries exceeded")
    raise TimeoutError("Max retries exceeded")
