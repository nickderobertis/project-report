from dataclasses import dataclass
from typing import Optional

import semver


@dataclass
class Version:
    major: Optional[int] = None
    minor: Optional[int] = None
    patch: Optional[int] = None
    prerelease: Optional[str] = None
    build: Optional[str] = None
    full_str: Optional[str] = None
    is_semver: bool = False

    def __post_init__(self):
        self._validate()

    def _validate(self):
        attrs = [
            "major",
            "minor",
            "patch",
            "prerelease",
            "build",
            "full_str",
        ]
        if all([getattr(self, attr) is None for attr in attrs]):
            raise ValueError(
                "must provide some version information, all attributes are None"
            )

    @property
    def semantic_version(self) -> semver.VersionInfo:
        if not self.is_semver:
            raise ValueError("is_semver=False, cannot create semver object")

        return semver.VersionInfo(
            major=self.major,
            minor=self.minor,
            patch=self.patch,
            prerelease=self.prerelease,
            build=self.build,
        )

    def __eq__(self, other):
        if not self.is_semver or isinstance(other, Version) and not other.is_semver:
            return super().__eq__(other)
        if isinstance(other, Version):
            compare = other.semantic_version
        else:
            compare = other
        return self.semantic_version == compare

    def __lt__(self, other):
        if not self.is_semver:
            raise ValueError("cannot compare non-semantic versions")
        if isinstance(other, Version):
            compare = other.semantic_version
        else:
            compare = other
        return self.semantic_version < compare

    def __le__(self, other):
        if not self.is_semver:
            raise ValueError("cannot compare non-semantic versions")
        if isinstance(other, Version):
            compare = other.semantic_version
        else:
            compare = other
        return self.semantic_version <= compare

    def __gt__(self, other):
        if not self.is_semver:
            raise ValueError("cannot compare non-semantic versions")
        if isinstance(other, Version):
            compare = other.semantic_version
        else:
            compare = other
        return self.semantic_version > compare

    def __ge__(self, other):
        if not self.is_semver:
            raise ValueError("cannot compare non-semantic versions")
        if isinstance(other, Version):
            compare = other.semantic_version
        else:
            compare = other
        return self.semantic_version >= compare

    @classmethod
    def from_str(cls, version: str) -> "Version":
        full_str = version
        if version.startswith("v") and version[1].isdigit():
            # Looks like could be semantic versioning but starting with v, strip the v
            # but keep it in full_str
            version = version[1:]

        sem_version: Optional[semver.VersionInfo] = None
        try:
            sem_version = semver.VersionInfo.parse(version)
        except ValueError as e:
            if "not valid SemVer string" not in str(e):
                raise e
        if sem_version is not None:
            return cls.from_semver_version(sem_version, full_str=full_str)

        # Not semantic versioning, don't parse it
        return cls(full_str=full_str)

    @classmethod
    def from_semver_version(
        cls, version: semver.VersionInfo, full_str: Optional[str] = None
    ) -> "Version":
        return cls(
            major=version.major,
            minor=version.minor,
            patch=version.patch,
            prerelease=version.prerelease,
            build=version.build,
            full_str=full_str,
            is_semver=True,
        )

    def __str__(self) -> str:
        if self.full_str is not None:
            return self.full_str

        return str(self.semantic_version)
