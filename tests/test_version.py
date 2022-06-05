import pytest
import semver

from projectreport.version import Version


def test_version_from_semver_str():
    version1 = Version.from_str("3.4.5-pre.2+build.4")
    version2 = Version.from_str("v3.4.5-pre.2+build.4")
    for version in [version1, version2]:
        assert version.major == 3
        assert version.minor == 4
        assert version.patch == 5
        assert version.prerelease == "pre.2"
        assert version.build == "build.4"
        assert version.is_semver
        assert version.semantic_version == semver.VersionInfo.parse(
            "3.4.5-pre.2+build.4"
        )
    assert str(version1) == version1.full_str == "3.4.5-pre.2+build.4"
    assert str(version2) == version2.full_str == "v3.4.5-pre.2+build.4"


def test_version_from_non_semver_str():
    version1 = Version.from_str("3")
    version2 = Version.from_str("v3")
    for version in [version1, version2]:
        assert version.major is None
        assert version.minor is None
        assert version.patch is None
        assert version.prerelease is None
        assert version.build is None
        assert not version.is_semver
        with pytest.raises(ValueError) as excinfo:
            stuff = version.semantic_version
        assert "is_semver=False" in excinfo.exconly()
    assert str(version1) == version1.full_str == "3"
    assert str(version2) == version2.full_str == "v3"


def test_compare_versions():
    version1 = Version.from_str("1.0.0")
    version2 = Version.from_str("1.0.1")
    version3 = Version.from_str("1.0.0")
    not_semver = Version.from_str("blah")
    assert version1 < version2
    assert version1 <= version2
    assert version2 > version1
    assert version2 >= version1
    assert version1 == version3
    assert version1 == semver.VersionInfo.parse("1.0.0")
    assert version1 == "1.0.0"
    assert not version1 == not_semver
    assert not version2 == not_semver
    assert not version3 == not_semver

    for version in [version1, version2, version3]:
        with pytest.raises(ValueError) as excinfo:
            version > not_semver
        assert "is_semver=False, cannot create semver object" in str(excinfo)
        with pytest.raises(ValueError) as excinfo:
            not_semver > version
        assert "cannot compare non-semantic versions" in str(excinfo)

        with pytest.raises(ValueError) as excinfo:
            version >= not_semver
        assert "is_semver=False, cannot create semver object" in str(excinfo)
        with pytest.raises(ValueError) as excinfo:
            not_semver >= version
        assert "cannot compare non-semantic versions" in str(excinfo)

        with pytest.raises(ValueError) as excinfo:
            version < not_semver
        assert "is_semver=False, cannot create semver object" in str(excinfo)
        with pytest.raises(ValueError) as excinfo:
            not_semver < version
        assert "cannot compare non-semantic versions" in str(excinfo)

        with pytest.raises(ValueError) as excinfo:
            version <= not_semver
        assert "is_semver=False, cannot create semver object" in str(excinfo)
        with pytest.raises(ValueError) as excinfo:
            not_semver <= version
        assert "cannot compare non-semantic versions" in str(excinfo)
