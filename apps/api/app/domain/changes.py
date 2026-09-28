"""Changes a user can request on the CV (Command pattern).

A change request (.md/.txt) is parsed into a list of these commands; each one knows how to
apply itself to the aggregate. New kinds of change are new classes, existing ones stay closed.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from app.domain.models import (
    Course,
    CurriculumVitae,
    Education,
    Experience,
    OfficialCertification,
)


@dataclass(frozen=True)
class CertificateAttachment:
    """A certificate file the user points to; it becomes public once imported."""

    source: str
    folder: str


class CurriculumChange(ABC):
    @abstractmethod
    def apply(self, cv: CurriculumVitae) -> None: ...

    @abstractmethod
    def describe(self) -> str: ...

    def attachment(self) -> CertificateAttachment | None:
        return None

    def attach(self, file_path: str) -> None:
        """Receives the public path of the imported certificate."""


@dataclass
class _CertifiedChange(CurriculumChange, ABC):
    certificate: CertificateAttachment | None = field(default=None, kw_only=True)
    file_path: str | None = field(default=None, kw_only=True)

    def attachment(self) -> CertificateAttachment | None:
        return self.certificate

    def attach(self, file_path: str) -> None:
        self.file_path = file_path


@dataclass
class AddCourse(_CertifiedChange):
    title: str
    category: str
    hours: int | None = None

    def apply(self, cv: CurriculumVitae) -> None:
        cv.add_course(self.category, Course(self.title, self.hours, self.file_path))

    def describe(self) -> str:
        return f"Course added to '{self.category}': {self.title}"


@dataclass
class AddLearningPath(_CertifiedChange):
    title: str
    hours: int | None = None

    def apply(self, cv: CurriculumVitae) -> None:
        cv.add_learning_path(Course(self.title, self.hours, self.file_path))

    def describe(self) -> str:
        return f"Learning path added: {self.title}"


@dataclass
class AddOfficialCertification(_CertifiedChange):
    title: str
    issuer: str
    color: str = OfficialCertification.DEFAULT_COLOR
    icon: str = OfficialCertification.DEFAULT_ICON

    def apply(self, cv: CurriculumVitae) -> None:
        cv.add_official_certification(
            OfficialCertification(self.title, self.issuer, self.color, self.icon, self.file_path)
        )

    def describe(self) -> str:
        return f"Official certification added: {self.title} — {self.issuer}"


@dataclass
class RemoveTraining(CurriculumChange):
    title: str

    def apply(self, cv: CurriculumVitae) -> None:
        cv.remove_training(self.title)

    def describe(self) -> str:
        return f"Training removed: {self.title}"


@dataclass
class AddExperience(CurriculumChange):
    experience: Experience

    def apply(self, cv: CurriculumVitae) -> None:
        cv.add_experience(self.experience)

    def describe(self) -> str:
        return f"Experience added: {self.experience.role} at {self.experience.company}"


@dataclass
class AddEducation(CurriculumChange):
    education: Education

    def apply(self, cv: CurriculumVitae) -> None:
        cv.add_education(self.education)

    def describe(self) -> str:
        return f"Education added: {self.education.degree} ({self.education.institution})"


@dataclass
class AddSkillItems(CurriculumChange):
    category: str
    items: list[str]

    def apply(self, cv: CurriculumVitae) -> None:
        cv.add_skill_items(self.category, self.items)

    def describe(self) -> str:
        return f"Skills added to '{self.category}': {', '.join(self.items)}"


@dataclass
class SetLanguage(CurriculumChange):
    lang: str
    level: str

    def apply(self, cv: CurriculumVitae) -> None:
        cv.set_language(self.lang, self.level)

    def describe(self) -> str:
        return f"Language set: {self.lang} ({self.level})"


@dataclass
class UpdateProfile(CurriculumChange):
    profile: str

    def apply(self, cv: CurriculumVitae) -> None:
        cv.set_profile(self.profile)

    def describe(self) -> str:
        return "Professional profile updated"


@dataclass
class UpdatePersonalField(CurriculumChange):
    field_name: str
    value: str

    def apply(self, cv: CurriculumVitae) -> None:
        cv.update_personal(self.field_name, self.value)

    def describe(self) -> str:
        return f"Personal data updated: {self.field_name}"
