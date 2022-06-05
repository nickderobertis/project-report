import warnings
from copy import deepcopy
from datetime import datetime, timedelta
from typing import Callable, Dict, List, Optional, Union

import dateutil
import pandas as pd
from dateutil import parser as dateparser
from github.Commit import Commit
from github.CommitStats import CommitStats
from github.GitAuthor import GitAuthor
from github.GitCommit import GitCommit
from github.GitRelease import GitRelease
from github.Issue import Issue
from github.NamedUser import NamedUser
from github.Repository import Repository
from github.Stargazer import Stargazer

from projectreport.analyzer.ts.base import TimeSeriesAnalysis
from projectreport.analyzer.ts.types import DictList
from projectreport.tools.monkey_patch_github import (
    NoMorePagesAllowedException,
    monkey_patch_github_obj_for_throttling,
)
from projectreport.version import (
    add_major_minor_patch_changed_to_df,
    add_major_minor_patch_to_df,
)


class GithubAnalysis(TimeSeriesAnalysis):
    analysis_attrs = ["repo"]

    def __init__(self, repo: Repository, auto_throttle: bool = True):
        self.repo = deepcopy(repo)
        self.auto_throttle = auto_throttle
        if self.auto_throttle:
            monkey_patch_github_obj_for_throttling(self.repo)

    @property
    def event_functions(self) -> Dict[str, Callable[[Repository], DictList]]:
        funcs: Dict[str, Callable[[Repository], DictList]] = dict(
            commits=commit_stats_from_repo,
            issues=issue_stats_from_repo,
            stars=stars_from_repo,
            releases=releases_from_repo,
        )
        return funcs

    @property
    def count_functions(self) -> Dict[str, Callable[[DictList, str], DictList]]:
        funcs: Dict[str, Callable[[DictList, str], DictList]] = dict(
            commits=commit_loc_counts_from_commit_events,
            issues=issue_counts_from_issue_events,
            stars=star_counts_from_star_events,
            releases=release_counts_from_release_events,
        )
        return funcs


def commit_stats_from_repo(repo: Repository, author_stats: bool = True) -> DictList:
    all_data = []
    commit: Commit
    try:
        for commit in repo.get_commits():
            stats: CommitStats = commit.stats
            author: Optional[Union[NamedUser, GitAuthor]] = _get_author_from_commit(
                commit
            )
            committer: Optional[
                Union[NamedUser, GitAuthor]
            ] = _get_committer_from_commit(commit)
            data_dict = dict(
                sha=commit.sha,
                last_modified=dateparser.parse(commit.last_modified)
                if commit.last_modified is not None
                else None,
                additions=stats.additions,
                deletions=stats.deletions,
                url=commit.html_url,
            )
            if author_stats:
                if author is not None:
                    data_dict.update(_get_data_from_named_user_or_git_author(author))
                if committer is not None:
                    data_dict.update(
                        _get_data_from_named_user_or_git_author(
                            committer, is_committer=True
                        )
                    )
            all_data.append(data_dict)
    except NoMorePagesAllowedException:
        warnings.warn(
            f"Could not collect full history for {repo.name} commits as Github "
            f"limits the amount of history than can be pulled"
        )

    return all_data  # type: ignore


def commit_loc_counts_from_commit_events(
    commits: DictList, freq: str = "d"
) -> DictList:
    event_df = pd.DataFrame(commits)
    event_df["net"] = event_df["additions"] - event_df["deletions"]
    event_df["change"] = event_df["additions"] + event_df["deletions"]
    start = _get_end_of_period(event_df["last_modified"].min(), freq)
    end = event_df["last_modified"].max()

    dates = pd.date_range(start=start, end=end, freq=freq)
    count_data = []
    for date in dates:
        until_time_df = event_df[event_df["last_modified"] < date]
        commit_counts = len(until_time_df)
        loc = until_time_df["net"].sum()
        loc_changed = until_time_df["change"].sum()
        count_data.append(
            dict(date=date, commits=commit_counts, loc=loc, loc_changed=loc_changed)
        )
    return count_data


def issue_stats_from_repo(repo: Repository) -> DictList:
    all_data = []
    issue: Issue
    try:
        for issue in repo.get_issues(state="all"):
            data_dict = dict(
                number=issue.number,
                created_at=issue.created_at,
                updated_at=issue.updated_at,
                closed_at=issue.closed_at,
                comments_count=issue.comments,
                state=issue.state,
                is_pull_issue=issue.pull_request is not None,
            )
            all_data.append(data_dict)
    except NoMorePagesAllowedException:
        warnings.warn(
            f"Could not collect full history for {repo.name} issues as Github "
            f"limits the amount of history than can be pulled"
        )

    return all_data  # type: ignore


def issue_counts_from_issue_events(issues: DictList, freq: str = "d") -> DictList:
    event_df = pd.DataFrame(issues)
    start = _get_end_of_period(event_df["created_at"].min(), freq)
    end = event_df["updated_at"].max()
    dates = pd.date_range(start=start, end=end, freq=freq)
    count_data = []
    for date in dates:
        until_time_df = event_df.loc[event_df["created_at"] <= date]
        # Mark issues which are closed now as open if they were not closed by this time
        until_time_df.loc[until_time_df["closed_at"] > date, "state"] = "open"

        pull_df = until_time_df[until_time_df["is_pull_issue"]]
        issue_df = until_time_df[~until_time_df["is_pull_issue"]]

        all_issues = len(until_time_df)
        closed_issues = len(issue_df[issue_df["state"] == "closed"])
        closed_pull_issues = len(pull_df[pull_df["state"] == "closed"])
        open_issues = len(issue_df[issue_df["state"] == "open"])
        open_pull_issues = len(pull_df[pull_df["state"] == "open"])

        count_data.append(
            dict(
                date=date,
                all_issues=all_issues,
                closed_issues=closed_issues,
                closed_pull_issues=closed_pull_issues,
                open_issues=open_issues,
                open_pull_issues=open_pull_issues,
            )
        )

    return count_data


def stars_from_repo(repo: Repository) -> DictList:
    all_data = []
    stars: Stargazer
    try:
        for stars in repo.get_stargazers_with_dates():
            user: NamedUser = stars.user
            data_dict = dict(
                date=stars.starred_at,
                user_name=user.name,
                user_login=user.login,
            )
            all_data.append(data_dict)
    except NoMorePagesAllowedException:
        warnings.warn(
            f"Could not collect full history for {repo.name} stars as Github "
            f"limits the amount of history than can be pulled"
        )

    return all_data  # type: ignore


def star_counts_from_star_events(stars: DictList, freq: str = "d") -> DictList:
    event_df = pd.DataFrame(stars)
    start = _get_end_of_period(event_df["date"].min(), freq)
    end = event_df["date"].max()

    dates = pd.date_range(start=start, end=end, freq=freq)
    count_data = []
    for date in dates:
        until_time_df = event_df[event_df["date"] < date]
        star_count = len(until_time_df)
        count_data.append(dict(date=date, stars=star_count))

    return count_data


def releases_from_repo(repo: Repository) -> DictList:
    all_data = []
    releases: GitRelease
    try:
        for release in repo.get_releases():
            author = release.author
            author_name: Optional[str] = None
            author_login: Optional[str] = None
            if author is not None:
                author_name = author.name
                author_login = author.login
            data_dict = dict(
                created_at=release.created_at,
                published_at=release.published_at,
                url=release.html_url,
                id=release.id,
                tag_name=release.tag_name,
                draft=release.draft,
                prerelease=release.prerelease,
                body=release.body,
                author_name=author_name,
                author_login=author_login,
            )
            all_data.append(data_dict)
    except NoMorePagesAllowedException:
        warnings.warn(
            f"Could not collect full history for {repo.name} releases as Github "
            f"limits the amount of history than can be pulled"
        )

    return all_data  # type: ignore


def release_counts_from_release_events(
    releases: DictList,
    freq: str = "d",
    date_var: str = "published_at",
) -> DictList:
    event_df = pd.DataFrame(releases)
    event_df.sort_values(date_var, inplace=True)
    start = _get_end_of_period(event_df[date_var].min(), freq)
    end = event_df[date_var].max()
    add_major_minor_patch_to_df(event_df)

    semver_df = event_df.loc[event_df["Version"].apply(lambda ver: ver.is_semver)]
    if not semver_df.empty:
        add_major_minor_patch_changed_to_df(semver_df)

    dates = pd.date_range(start=start, end=end, freq=freq)
    count_data = []
    for date in dates:
        until_time_df = event_df[event_df[date_var] < date]
        release_count = len(until_time_df)
        until_time_df = semver_df[semver_df[date_var] < date]
        if not until_time_df.empty:
            major_df = until_time_df[until_time_df["Major Changed"]]
            major_count = len(major_df)
            minor_df = until_time_df[until_time_df["Minor Changed"]]
            minor_count = len(minor_df)
            patch_df = until_time_df[until_time_df["Patch Changed"]]
            patch_count = len(patch_df)
        else:
            major_count, minor_count, patch_count = 0, 0, 0
        count_data.append(
            dict(
                date=date,
                releases=release_count,
                major_releases=major_count,
                minor_releases=minor_count,
                patch_releases=patch_count,
            )
        )

    return count_data


def _get_data_from_named_user_or_git_author(
    user: Union[NamedUser, GitAuthor], is_committer: bool = False
) -> Dict[str, str]:
    if is_committer:
        key_base = "committer"
    else:
        key_base = "author"

    data: Dict[str, str] = {
        f"{key_base}_name": user.name,
        f"{key_base}_email": user.email,
    }

    if isinstance(user, NamedUser):
        data.update(
            {
                f"{key_base}_login": user.login,
            }
        )

    return data


def _get_author_from_commit(commit: Commit) -> Optional[Union[NamedUser, GitAuthor]]:
    if commit.author is not None:
        # NamedUser
        return commit.author

    git_commit: GitCommit = commit.commit
    # GitAuthor
    return git_commit.author


def _get_committer_from_commit(commit: Commit) -> Optional[Union[NamedUser, GitAuthor]]:
    if commit.committer is not None:
        # NamedUser
        return commit.committer

    git_commit: GitCommit = commit.commit
    # GitAuthor
    return git_commit.committer


def _get_end_of_period(date: pd.Timestamp, freq: str) -> pd.Timestamp:
    # TODO [#16]: get _get_end_of_period working correctly for all frequencies
    #
    # Works correctly for month, day, hour, and weeks starting on a different day.
    # Currently gets beginning of period for weeks starting with the same day.
    try:
        return date.ceil(freq)
    except ValueError as e:
        if "is a non-fixed frequency" in str(e):
            return date.to_period(freq).to_timestamp(freq).tz_localize("UTC")
        else:
            raise e
