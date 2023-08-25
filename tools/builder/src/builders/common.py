from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class Error(Enum):
    SUCCESS = 1
    IO_ERROR = auto()
    BUILD_TOOL_ERROR = auto()
    HEADER_NOT_FOUND = auto()
    LINKED_DEP_NOT_FOUND = auto()
    FILE_MISSING = auto()
    FILE_COPY_FAILED = auto()
    FILE_EXISTS_WARNING = auto()


@dataclass
class Result(object):
    error: Error = Error.SUCCESS
    result: Any = None


class Builder():
    def __init__(self, root_path: Path, deps: list, name: str):
        self.root_path: Path = root_path
        self.deps: dict = deps
        self.name: str = name

        self.build_dir: Path = self.deps[self.name] / 'build'
        self.include_dir: Path = self.deps[self.name] / 'include'

        self.target_build_dir: Path = self.root_path / 'deps' / self.name / 'build'
        self.target_include_dir: Path = self.root_path / 'deps' / self.name / 'include'

    def prepare(self) -> Result:
        return Result(Error.SUCCESS, None)

    def build(self) -> Result:
        return Result(Error.SUCCESS, None)

    def clean(self) -> Result:
        return Result(Error.SUCCESS, None)
