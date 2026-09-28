"""Domain errors raised when a change or a CV state breaks a business rule."""

from __future__ import annotations


class CurriculumError(Exception):
    """Base class for every error the CV backend reports to the user."""


class DuplicateEntryError(CurriculumError):
    def __init__(self, title: str) -> None:
        super().__init__(f"'{title}' already exists in the CV")
        self.title = title


class EntryNotFoundError(CurriculumError):
    def __init__(self, what: str) -> None:
        super().__init__(f"{what} was not found in the CV")


class InvalidCurriculumError(CurriculumError):
    def __init__(self, problems: list[str]) -> None:
        details = "\n".join(f"  - {problem}" for problem in problems)
        super().__init__(f"The CV has {len(problems)} problem(s):\n{details}")
        self.problems = problems
