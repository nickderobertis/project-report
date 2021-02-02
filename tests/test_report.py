import datetime
import os
from copy import deepcopy

import pytz

from tests.base import get_project_report, REPORTS_FOLDER, git_project

GENERATE_REPORTS = False


def test_report(git_project):
    # Same created, later name
    gp2 = deepcopy(git_project)
    gp2.data['name'] = 'zgitrepo'

    # Later created, earlier name
    gp3 = deepcopy(git_project)
    gp3.data['name'] = 'agitrepo'
    eastern = pytz.timezone('US/Eastern')
    gp3.data['created'] = datetime.datetime(2020, 2, 1, 13, 0, 0, 0, tzinfo=eastern)

    report = get_project_report(add_projects=[gp2, gp3, git_project])

    attr_extensions = dict(
        json='json',
        yaml='yml',
        latex='tex',
    )

    for attr, extension in attr_extensions.items():
        report_outpath = os.path.join(REPORTS_FOLDER, f'report.{extension}')
        report_body = getattr(report, attr)
        if GENERATE_REPORTS:
            with open(report_outpath, 'w') as f:
                f.write(report_body)
        else:
            with open(report_outpath, 'r') as f:
                expected_report_body = f.read()
            assert report_body == expected_report_body