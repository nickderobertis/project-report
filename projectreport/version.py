from dataclasses import dataclass
from typing import Optional, Tuple

import pandas as pd
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


def major_minor_patch(
    version: Version,
) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    if not version.is_semver:
        return None, None, None
    return version.major, version.minor, version.patch


def add_major_minor_patch_to_df(df: pd.DataFrame, version_col: str = "tag_name"):
    df["Version"] = df[version_col].apply(lambda tag: Version.from_str(tag))
    df["Major"], df["Minor"], df["Patch"] = zip(*df["Version"].map(major_minor_patch))


def add_major_minor_patch_changed_to_df(df: pd.DataFrame):
    df["Max Version"] = df["Version"].cummax()
    df["Max Major"], df["Max Minor"], df["Max Patch"] = zip(
        *df["Max Version"].map(major_minor_patch)
    )
    for col in ["Major", "Minor", "Patch"]:
        df[f"Max {col}"] = df[f"Max {col}"].shift()
        df[f"{col} Diff"] = df[col] - df[f"Max {col}"]
    df["Major Changed"] = False
    df.loc[
        (~pd.isnull(df["Major Diff"])) & (df["Major Diff"] != 0), "Major Changed"
    ] = True
    df["Minor Changed"] = False
    df.loc[
        (~pd.isnull(df["Minor Diff"]))
        & (df["Minor Diff"] != 0)
        & (~df["Major Changed"]),
        "Minor Changed",
    ] = True
    df["Patch Changed"] = False
    df.loc[
        (~pd.isnull(df["Patch Diff"]))
        & (df["Patch Diff"] != 0)
        & (~df["Minor Changed"])
        & (~df["Major Changed"]),
        "Patch Changed",
    ] = True
