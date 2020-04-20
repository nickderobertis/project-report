from datetime import timezone, datetime
import time
import types

from github import RateLimitExceededException
from github.GithubObject import GithubObject
from github.RateLimit import RateLimit
from github.Requester import Requester

from projectreport.logger import logger


def monkey_patch_github_obj_for_throttling(gh_obj: GithubObject):
    gh_obj._requester._Requester__check = types.MethodType(__check_patched_for_throttling, gh_obj._requester)


def __check_patched_for_throttling(obj: Requester, status, responseHeaders, output):
    logger.debug('made request')
    output = obj._Requester__structuredFromJson(output)
    if status >= 400:
        exc = obj._Requester__createException(status, responseHeaders, output)
        if isinstance(exc, RateLimitExceededException):
            headers, data = obj.requestJsonAndCheck("GET", "/rate_limit")
            limits = RateLimit(obj, headers, data["resources"], True)
            reset = limits.search.reset.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            seconds = (reset - now).total_seconds()
            logger.info(f"Rate limit exceeded")
            logger.info(f"Reset is in {seconds:.3g} seconds.")
            if seconds > 0.0:
                logger.info(f"Waiting for {seconds:.3g} seconds...")
                time.sleep(seconds)
                logger.info("Done waiting - resume!")
        else:
            raise exc
    return responseHeaders, output