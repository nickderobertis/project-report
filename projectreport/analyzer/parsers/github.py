from os import getenv
from typing import Any, Dict, Optional, Sequence, Tuple, TypedDict

import github.GithubException
from cached_property import cached_property
from github import Github

from projectreport.analyzer.parsers.base import Parser
from projectreport.analyzer.parsers.data_types import ParserDataType
from projectreport.analyzer.parsers.url import URLParser
from projectreport.tools.monkey_patch_github import (
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


class GithubParser(URLParser):
    def __init__(self, path: str):
        self.repo_key = _github_url_to_owner_and_name(path)
        self.github_repo = gh.get_repo(self.repo_key)
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
        data = GithubData(
            name=self.github_repo.name,
            description=self.github_repo.description,
            version=None,
        )
        try:
            release = self.github_repo.get_latest_release()
        except github.UnknownObjectException:
            pass
        else:
            if release is not None:
                data["version"] = release.tag_name
        return data

    @cached_property
    def docstring(self) -> Optional[str]:
        if self.parsed is None:
            return None
        return self.parsed.get("description")

    @cached_property
    def version(self) -> Optional[Version]:
        if self.parsed is None:
            return None
        version_str = self.parsed.get("version")
        if version_str is None:
            return None
        return Version.from_str(version_str)

    @classmethod
    def matches_path(cls, path: str) -> bool:
        return "github.com" in path


def _github_url_to_owner_and_name(url: str) -> str:
    if "github.com" not in url:
        raise ValueError(f"got a non-Github URL {url}")
    return "/".join(url.split("/")[-2:])
