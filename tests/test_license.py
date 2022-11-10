from projectreport.license.finder import find_license_file
from projectreport.license.model import LicenseType
from projectreport.license.parsing import license_text_to_license
from tests.config import APACHE_LICENSE_PATH, GPL_LICENSE_PATH, MIT_LICENSE_PATH


def test_parse_mit_license():
    license_text = MIT_LICENSE_PATH.read_text()
    license = license_text_to_license(license_text)
    assert license.type == LicenseType.MIT
    assert license.text == license_text


def test_parse_apache_license():
    license_text = APACHE_LICENSE_PATH.read_text()
    license = license_text_to_license(license_text)
    assert license.type == LicenseType.APACHE
    assert license.text == license_text


def test_parse_gpl_license():
    license_text = GPL_LICENSE_PATH.read_text()
    license = license_text_to_license(license_text)
    assert license.type == LicenseType.GPL
    assert license.text == license_text


def test_find_license_md_file():
    license_file = find_license_file(MIT_LICENSE_PATH.parent)
    assert license_file == MIT_LICENSE_PATH


def test_find_license_txt_file():
    license_file = find_license_file(APACHE_LICENSE_PATH.parent)
    assert license_file == APACHE_LICENSE_PATH


def test_find_copying_file():
    license_file = find_license_file(GPL_LICENSE_PATH.parent)
    assert license_file == GPL_LICENSE_PATH
