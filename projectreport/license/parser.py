from typing import Optional

from projectreport.license.model import License, LicenseType
from projectreport.tools.text import get_first_non_empty_line_of_text


def license_text_to_license(license_text: str) -> Optional[License]:
    """Convert a license text to a License object."""
    license_type = _license_text_to_license_type(license_text)
    if license_type is None:
        return None
    license = License(license_type, license_text)
    return license


def _license_text_to_license_type(license_text: str) -> Optional[LicenseType]:
    """
    Convert a license text to a LicenseType object.

    TODO: This is very much a hack that will not work with license variations
    """
    first_line = get_first_non_empty_line_of_text(license_text).casefold()
    if first_line is None:
        return None

    if "mit" in first_line:
        return LicenseType.MIT
    if "bsd" in first_line:
        return LicenseType.BSD
    if "lgpl" in first_line or "lesser general public license" in first_line:
        return LicenseType.LGPL
    if "agpl" in first_line or "affero general public license" in first_line:
        return LicenseType.AGPL
    if "gpl" in first_line or "general public license" in first_line:
        return LicenseType.GPL
    if "mpl" in first_line or "mozilla public license" in first_line:
        return LicenseType.MPL
    if "apache" in first_line:
        return LicenseType.APACHE
    return None
