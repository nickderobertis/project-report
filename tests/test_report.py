import os

from tests.base import get_project_report, REPORTS_FOLDER


def test_report():
    report = get_project_report()

    attr_extensions = dict(
        json='json',
        yaml='yml',
        latex='tex',
    )

    for attr, extension in attr_extensions.items():
        report_outpath = os.path.join(REPORTS_FOLDER, f'report.{extension}')
        report_body = getattr(report, attr)
        with open(report_outpath, 'r') as f:
            expected_report_body = f.read()
        assert report_body == expected_report_body