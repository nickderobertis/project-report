"""
Generates reports for test data
"""
import os

from tests.base import REPORTS_FOLDER, get_project_report


def generate_reports():
    report = get_project_report()

    attr_extensions=dict(
        json='json',
        yaml='yml',
        latex='tex',
    )

    for attr, extension in attr_extensions.items():
        report_outpath = os.path.join(REPORTS_FOLDER, f'report.{extension}')
        report_body = getattr(report, attr)
        with open(report_outpath, 'w') as f:
            f.write(report_body)


if __name__ == '__main__':
    generate_reports()
