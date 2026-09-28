"""CV aggregate and value objects. Pure Python: no files, no formats, no frameworks."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field, fields
from typing import Iterator

from app.domain.errors import DuplicateEntryError, EntryNotFoundError


@dataclass
class PersonalInfo:
    name: str
    title: str
    email: str
    phone1: str
    phone2: str
    location: str
    linkedin: str
    github: str
    portfolio: str
    birth_date: str

    @classmethod
    def editable_fields(cls) -> tuple[str, ...]:
        return tuple(f.name for f in fields(cls))


@dataclass
class SkillCategory:
    category: str
    items: str

    def item_names(self) -> list[str]:
        return [item.strip() for item in self.items.split(",") if item.strip()]

    def add_items(self, new_items: list[str]) -> None:
        known = {item.casefold() for item in self.item_names()}
        additions = [item for item in new_items if item.casefold() not in known]
        if additions:
            self.items = ", ".join([*self.item_names(), *additions])


@dataclass
class Experience:
    company: str
    role: str
    period: str
    bullets: list[str]
    technologies: list[str] = field(default_factory=list)


@dataclass
class Education:
    degree: str
    institution: str
    year: str


@dataclass
class Course:
    """A course or learning path. `file_path` is the public path of its certificate, if any."""

    title: str
    hours: int | None = None
    file_path: str | None = None


@dataclass
class OfficialCertification:
    DEFAULT_COLOR = "border-blue-500 bg-blue-50"
    DEFAULT_ICON = "🏅"

    title: str
    issuer: str
    color: str = DEFAULT_COLOR
    icon: str = DEFAULT_ICON
    file_path: str | None = None


@dataclass
class Language:
    lang: str
    level: str


@dataclass
class CurriculumVitae:
    """Aggregate root: every change to the CV goes through these methods."""

    personal: PersonalInfo
    profile: str
    skills: list[SkillCategory]
    experience: list[Experience]
    education: list[Education]
    official_certifications: list[OfficialCertification]
    courses_by_category: dict[str, list[Course]]
    learning_paths: list[Course]
    languages: list[Language]

    # ── queries ──────────────────────────────────────────────

    def training_titles(self) -> Iterator[str]:
        yield from (cert.title for cert in self.official_certifications)
        yield from (course.title for course in self.learning_paths)
        for courses in self.courses_by_category.values():
            yield from (course.title for course in courses)

    def certificate_paths(self) -> Iterator[str]:
        entries = [*self.official_certifications, *self.learning_paths]
        entries += [course for courses in self.courses_by_category.values() for course in courses]
        yield from (entry.file_path for entry in entries if entry.file_path)

    def fingerprint(self) -> str:
        """Stable content hash shared by the JSON, the PDFs and the DOCX of one generation."""
        canonical = json.dumps(asdict(self), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    # ── commands ─────────────────────────────────────────────

    def _ensure_new_training(self, title: str) -> None:
        if any(existing.casefold() == title.casefold() for existing in self.training_titles()):
            raise DuplicateEntryError(title)

    def add_course(self, category: str, course: Course) -> None:
        self._ensure_new_training(course.title)
        self.courses_by_category.setdefault(category, []).append(course)

    def add_learning_path(self, course: Course) -> None:
        self._ensure_new_training(course.title)
        self.learning_paths.append(course)

    def add_official_certification(self, certification: OfficialCertification) -> None:
        self._ensure_new_training(certification.title)
        self.official_certifications.append(certification)

    def remove_training(self, title: str) -> None:
        key = title.casefold()
        for collection in (self.official_certifications, self.learning_paths, *self.courses_by_category.values()):
            for entry in collection:
                if entry.title.casefold() == key:
                    collection.remove(entry)
                    self.courses_by_category = {
                        category: courses for category, courses in self.courses_by_category.items() if courses
                    }
                    return
        raise EntryNotFoundError(f"Training '{title}'")

    def add_experience(self, experience: Experience) -> None:
        """Newest experience goes first, as in the rendered CV."""
        self.experience.insert(0, experience)

    def add_education(self, education: Education) -> None:
        self.education.insert(0, education)

    def add_skill_items(self, category: str, items: list[str]) -> None:
        for skill in self.skills:
            if skill.category.casefold() == category.casefold():
                skill.add_items(items)
                return
        self.skills.append(SkillCategory(category=category, items=", ".join(items)))

    def set_language(self, lang: str, level: str) -> None:
        for language in self.languages:
            if language.lang.casefold() == lang.casefold():
                language.level = level
                return
        self.languages.append(Language(lang=lang, level=level))

    def set_profile(self, profile: str) -> None:
        self.profile = profile

    def update_personal(self, field_name: str, value: str) -> None:
        if field_name not in PersonalInfo.editable_fields():
            raise EntryNotFoundError(f"Personal field '{field_name}'")
        setattr(self.personal, field_name, value)
