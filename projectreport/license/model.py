from enum import Enum


class LicenseType(str, Enum):
    MIT = "MIT"
    BSD = "BSD"
    GPL = "GPL"
    LGPL = "LGPL"
    AGPL = "AGPL"
    MPL = "MPL"
    APACHE = "APACHE"


class License:
    def __init__(self, license_type: LicenseType, text: str):
        self.type = license_type
        self.text = text

    def __repr__(self):
        return f"License({self.type})"
