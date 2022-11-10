from os import getenv
from typing import Any, Dict, List, Optional, Sequence, Tuple, TypedDict

import github.GithubException
from cached_property import cached_property
from github import Github
from github.Repository import Repository

from projectreport.analyzer.parsers.base import Parser
from projectreport.analyzer.parsers.data_types import ParserDataType
from projectreport.analyzer.parsers.url import URLParser
from projectreport.license.model import License
from projectreport.logger import logger
from projectreport.tools.monkey_patch_github import (
    ResourceNotFoundException,
    monkey_patch_github_obj_for_throttling,
)
from projectreport.version import Version

access_token = getenv("GITHUB_TOKEN")

gh = Github(access_token)
monkey_patch_github_obj_for_throttling(gh)


class GithubData(TypedDict):
    name: str
    description: Optional[str]
    version: Optional[str]
    topics: Optional[List[str]]


class GithubParser(URLParser):
    def __init__(self, path: str):
        self.repo_key = _github_url_to_owner_and_name(path)
        self.github_repo = get_repo(self.repo_key)
        monkey_patch_github_obj_for_throttling(self.github_repo)
        super().__init__(path)

    @staticmethod
    def find_github_url(urls: Sequence[str]) -> Optional[str]:
        for url in urls:
            if "github.com" in url:
                return url
        return None

    @cached_property
    def contents(self) -> str:
        raise NotImplementedError

    @cached_property
    def file_name(self) -> str:
        return f"repo:github:{self.github_repo.name}"

    @cached_property
    def parsed(self) -> GithubData:
        return GithubData(
            name=self.github_repo.name,
            description=self.github_repo.description,
            version=self._get_version_str_from_repo(),
            topics=self.github_repo.get_topics(),
        )

    @cached_property
    def license(self) -> Optional[License]:
        # TODO: Implement getting license from Github
        return None

    def _get_version_str_from_repo(self) -> Optional[str]:
        try:
            release = self.github_repo.get_latest_release()
        except (github.UnknownObjectException, ResourceNotFoundException):
            return None
        else:
            if release is not None:
                return release.tag_name
        return None

    @cached_property
    def docstring(self) -> Optional[str]:
        return self.parsed.get("description")

    @cached_property
    def version(self) -> Optional[Version]:
        version_str = self.parsed.get("version")
        if version_str is None:
            return None
        return Version.from_str(version_str)

    @cached_property
    def topics(self) -> Optional[List[str]]:
        return self.parsed.get("topics")

    @classmethod
    def matches_path(cls, path: str) -> bool:
        return "github.com" in path


def get_repo(name: str) -> Repository:
    logger.info(f"Requesting details for repository {name}")
    return gh.get_repo(name)


def _github_url_to_owner_and_name(url: str) -> str:
    if "github.com" not in url:
        raise ValueError(f"got a non-Github URL {url}")
    return "/".join(url.split("/")[-2:])
