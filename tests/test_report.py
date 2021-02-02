import os

from tests.base import get_project_report, REPORTS_FOLDER, git_project

GENERATE_REPORTS = False


def test_report(git_project):
    report = get_project_report(add_projects=[git_project])

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