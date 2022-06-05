import time
import types
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Union

from github import Github, GithubException, RateLimitExceededException
from github.GithubObject import GithubObject
from github.Rate import Rate
from github.RateLimit import RateLimit
from github.Requester import Requester
from requests.exceptions import RequestException

from projectreport.logger import logger

RATE_LIMIT_PAD_SECONDS = 180
REQUEST_EXCEPTION_WAIT = 60


def monkey_patch_github_obj_for_throttling(gh_obj: Union[Github, GithubObject]):
    requester = _get_requester(gh_obj)
    orig_request_and_check = requester.requestJsonAndCheck

    def request_json_and_check_patched_for_throttling(
        obj: Requester,
        verb: str,
        url: str,
        retries_remaining: int = 3,
        collected_exceptions: Optional[List[Exception]] = None,
        **kwargs,
    ):
        if retries_remaining <= 0:
            raise GithubException(
                f"could not make github request after retries. Got errors {collected_exceptions}",
                {"exc": collected_exceptions},
                None,
            )
        if collected_exceptions is None:
            collected_exceptions = []

        logger.debug(f"made {verb} request to {url}")
        try:
            return orig_request_and_check(verb, url, **kwargs)
        except RateLimitExceededException as e:
            collected_exceptions.append(e)
            _get_rate_limit_and_wait(requester)
            return request_json_and_check_patched_for_throttling(
                obj,
                verb,
                url,
                retries_remaining=retries_remaining - 1,
                collected_exceptions=collected_exceptions,
                **kwargs,
            )
        except (RequestException, GithubException) as e:
            if "pagination is limited for this resource" in str(e).casefold():
                raise NoMorePagesAllowedException
            collected_exceptions.append(e)
            _wait_for_read_timeout(e)
            return request_json_and_check_patched_for_throttling(
                obj,
                verb,
                url,
                retries_remaining=retries_remaining - 1,
                collected_exceptions=collected_exceptions,
                **kwargs,
            )

    requester.requestJsonAndCheck = types.MethodType(  # type: ignore
        request_json_and_check_patched_for_throttling, requester
    )


def _wait_for_read_timeout(e: Union[RequestException, GithubException]):
    logger.warning(
        f"Got request/Github exception: {e}. Sleeping for {REQUEST_EXCEPTION_WAIT}s"
    )
    time.sleep(REQUEST_EXCEPTION_WAIT)
    logger.info(f"Resuming from read timeout sleep at {datetime.now()}")


def _get_rate_limit_and_wait(obj: Requester):
    headers, data = obj.requestJsonAndCheck("GET", "/rate_limit")
    if data is None:
        raise ValueError("got no data from request")
    limits = RateLimit(obj, headers, data["resources"], True)
    reset = _get_last_reset_datetime_utc(limits)
    now = datetime.now(timezone.utc)
    diff = reset - now
    seconds = diff.total_seconds()
    current_tz = datetime.utcnow().astimezone().tzinfo
    logger.info(f"Rate limit exceeded")
    logger.info(f"Reset is at {reset.astimezone(current_tz)}.")
    if seconds > 0.0:
        # Extra 10s to ensure it's ready
        logger.info(f"Waiting for {diff + timedelta(seconds=RATE_LIMIT_PAD_SECONDS)}")
        time.sleep(seconds + RATE_LIMIT_PAD_SECONDS)
        logger.info(f"Done waiting - resuming at {datetime.now()}")


def _get_last_reset_datetime_utc(limit: RateLimit) -> datetime:
    # For some reason integration_manifest and source_import are in the raw data
    # but not supported by RateLimit object
    limit_attrs = [
        "core",
        "search",
        "graphql",
        # 'integration_manifest',
        # 'source_import',
        "rate",
    ]
    all_resets = []
    for attr in limit_attrs:
        try:
            rate: Rate = getattr(limit, attr)
        except AttributeError:
            continue
        reset = rate.reset.replace(tzinfo=timezone.utc)
        all_resets.append(reset)
    if not all_resets:
        raise ValueError(
            f"no reset time in rate limit object: {limit} with data {limit.raw_data}"
        )

    last_reset = max(all_resets)
    return last_reset


def _get_requester(gh_obj: Union[Github, GithubObject]) -> Requester:
    if isinstance(gh_obj, Github):
        attr = "_Github__requester"
    else:
        attr = "_requester"
    requester: Requester = getattr(gh_obj, attr)
    return requester


class NoMorePagesAllowedException(Exception):
    pass
