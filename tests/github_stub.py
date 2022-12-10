"""
A set of stubs so that we don't need to hit real Github during tests

Usage: decorate a test function with @patch_github()
"""
import contextlib
from typing import Any, Dict, List, Optional, Tuple
from unittest.mock import patch

from projectreport.analyzer.parsers import github


class RequesterStub:
    def requestJsonAndCheck(
        self,
        verb: str,
        url: str,
        parameters: Optional[Dict[str, Any]] = ...,
        headers: Optional[Dict[str, str]] = ...,
        input: Optional[Any] = ...,
    ) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
        ...


class GitReleaseStub:
    """
    A stub for the GitRelease object in the pygithub library.
    """

    @property
    def tag_name(self) -> str:
        return "v1.0.0"


class GithubRepoStub:
    """
    A stub for the Repo object in the pygithub library
    """

    _requester = RequesterStub()

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return f"[Github repo stub] {self._name}"

    @property
    def description(self) -> str:
        return "Github repo stub description"

    def get_topics(self) -> List[str]:
        return ["stub-topic1", "stub-topic2"]

    def get_latest_release(self) -> GitReleaseStub:
        return GitReleaseStub()


class GithubStub:
    """
    A stub for the Github object in the pygithub library
    """

    _requester = RequesterStub()

    def __init__(self, name: str):
        self._name = name

    def get_repo(self, name: str) -> GithubRepoStub:
        return GithubRepoStub(name)


@contextlib.contextmanager
def patch_github():
    """
    A context manager to patch the Github object in the pygithub library
    """
    with patch.object(github, "gh", GithubStub("stub-project")):
        yield
