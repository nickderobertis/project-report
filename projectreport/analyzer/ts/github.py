from datetime import datetime, timedelta
from typing import Dict, Callable, Union, List

import dateutil
from dateutil import parser as dateparser
import pandas as pd
from github.NamedUser import NamedUser
from github.Repository import Repository
from github.Commit import Commit
from github.CommitStats import CommitStats
from github.Issue import Issue
from github.Stargazer import Stargazer

from projectreport.analyzer.ts.base import TimeSeriesAnalysis
from projectreport.analyzer.ts.types import DictList


class GithubAnalysis(TimeSeriesAnalysis):
    analysis_attrs = ['repo']

    def __init__(self, repo: Repository):
        self.repo = repo

    @property
    def event_functions(self) -> Dict[str, Callable[[Repository], DictList]]:
        funcs: Dict[str, Callable[[Repository], DictList]] = dict(
            commits=commit_stats_from_repo,
            issues=issue_stats_from_repo,
            stars=stars_from_repo,
        )
        return funcs

    @property
    def count_functions(self) -> Dict[str, Callable[[DictList, str], DictList]]:
        funcs: Dict[str, Callable[[DictList, str], DictList]] = dict(
            commits=commit_loc_counts_from_commit_events,
            issues=issue_counts_from_issue_events,
            stars=star_counts_from_star_events,
        )
        return funcs


def commit_stats_from_repo(repo: Repository) -> DictList:
    all_data = []
    commit: Commit
    for commit in repo.get_commits():
        stats: CommitStats = commit.stats
        author: NamedUser = commit.author
        data_dict = dict(
            sha=commit.sha,
            author_name=author.name,
            author_login=author.login,
            last_modified=dateparser.parse(commit.last_modified),
            additions=stats.additions,
            deletions=stats.deletions
        )
        all_data.append(data_dict)

    return all_data


def commit_loc_counts_from_commit_events(commits: DictList, freq: str = 'd') -> DictList:
    event_df = pd.DataFrame(commits)
    event_df['net'] = event_df['additions'] - event_df['deletions']
    event_df['change'] = event_df['additions'] + event_df['deletions']
    start = event_df['last_modified'].min()

    # TODO [$5e9588b31c086a00073641de]: should not necessarily add a day in GithubAnalyzer counts, depends on freq
    #
    # This is being added because events on the last day were not coming to the counts.
    # This kind of code is in every time-series counts function
    end = event_df['last_modified'].max() + timedelta(days=1)

    dates = pd.date_range(start=start, end=end, freq=freq)
    count_data = []
    for date in dates:
        until_time_df = event_df[event_df['last_modified'] < date]
        commit_counts = len(until_time_df)
        loc = until_time_df['net'].sum()
        loc_changed = until_time_df['change'].sum()
        count_data.append(dict(
            date=date,
            commits=commit_counts,
            loc=loc,
            loc_changed=loc_changed
        ))
    return count_data


def issue_stats_from_repo(repo: Repository) -> DictList:
    all_data = []
    issue: Issue
    for issue in repo.get_issues(state='all'):
        data_dict = dict(
            number=issue.number,
            created_at=issue.created_at,
            updated_at=issue.updated_at,
            closed_at=issue.closed_at,
            comments_count=issue.comments,
            state=issue.state,
            is_pull_issue=issue.pull_request is not None
        )
        all_data.append(data_dict)

    return all_data


def issue_counts_from_issue_events(issues: DictList, freq: str = 'd') -> DictList:
    event_df = pd.DataFrame(issues)
    start = event_df['created_at'].min()
    end = event_df['updated_at'].max() + timedelta(days=1)
    dates = pd.date_range(start=start, end=end, freq=freq)
    count_data = []
    for date in dates:
        until_time_df = event_df.loc[event_df['created_at'] <= date]
        # Mark issues which are closed now as open if they were not closed by this time
        until_time_df.loc[until_time_df['closed_at'] > date, 'state'] = 'open'

        pull_df = until_time_df[until_time_df['is_pull_issue']]
        issue_df = until_time_df[~until_time_df['is_pull_issue']]

        all_issues = len(until_time_df)
        closed_issues = len(issue_df[issue_df['state'] == 'closed'])
        closed_pull_issues = len(pull_df[pull_df['state'] == 'closed'])
        open_issues = len(issue_df[issue_df['state'] == 'open'])
        open_pull_issues = len(pull_df[pull_df['state'] == 'open'])

        count_data.append(dict(
            date=date,
            all_issues=all_issues,
            closed_issues=closed_issues,
            closed_pull_issues=closed_pull_issues,
            open_issues=open_issues,
            open_pull_issues=open_pull_issues,
        ))

    return count_data


def stars_from_repo(repo: Repository) -> DictList:
    all_data = []
    stars: Stargazer
    for stars in repo.get_stargazers_with_dates():
        user: NamedUser = stars.user
        data_dict = dict(
            date=stars.starred_at,
            user_name=user.name,
            user_login=user.login,
        )
        all_data.append(data_dict)

    return all_data


def star_counts_from_star_events(stars: DictList, freq: str = 'd') -> DictList:
    event_df = pd.DataFrame(stars)
    start = event_df['date'].min()
    end = event_df['date'].max() + timedelta(days=1)

    dates = pd.date_range(start=start, end=end, freq=freq)
    count_data = []
    for date in dates:
        until_time_df = event_df[event_df['date'] < date]
        star_count = len(until_time_df)
        count_data.append(dict(
            date=date,
            stars=star_count
        ))

    return count_data
