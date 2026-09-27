"""Section types of a change request and how each one becomes a domain change.

Adding a new kind of request = adding a SectionBuilder subclass to DEFAULT_SECTIONS.
Keys are matched without accents or case, so `Categoría:` and `categoria:` are the same.
"""

from __future__ import annotations

import re
import unicodedata
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

from app.domain.changes import (
    AddCourse,
    AddEducation,
    AddExperience,
    AddLearningPath,
    AddOfficialCertification,
    AddSkillItems,
    CertificateAttachment,
    CurriculumChange,
    RemoveTraining,
    SetLanguage,
    UpdatePersonalField,
    UpdateProfile,
)
from app.domain.errors import CurriculumError
from app.domain.models import Education, Experience

FieldValue = str | list[str]


def normalize(text: str) -> str:
    stripped = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", stripped).strip().lower()


class RequestFormatError(CurriculumError):
    pass


@dataclass
class RawSection:
    name: str
    line: int
    base_dir: Path
    fields: dict[str, FieldValue] = field(default_factory=dict)

    @property
    def label(self) -> str:
        return f"'{self.name}' (line {self.line})"


class SectionReader:
    """Typed, validated access to the fields of one section."""

    def __init__(self, section: RawSection, aliases: dict[str, str]) -> None:
        self._section = section
        self._values: dict[str, FieldValue] = {}
        for key, value in section.fields.items():
            canonical = aliases.get(normalize(key))
            if canonical is None:
                allowed = ", ".join(sorted({k for k in aliases if k.isascii()}))
                raise RequestFormatError(f"{section.label}: unknown field '{key}'. Allowed: {allowed}")
            self._values[canonical] = value

    def text(self, key: str) -> str:
        value = self.optional_text(key)
        if not value:
            raise RequestFormatError(f"{self._section.label}: field '{key}' is required")
        return value

    def optional_text(self, key: str) -> str | None:
        value = self._values.get(key)
        if isinstance(value, list):
            value = " ".join(value)
        return value.strip() if value else None

    def items(self, key: str, *, required: bool = True) -> list[str]:
        value = self._values.get(key)
        items = value if isinstance(value, list) else [part for part in (value or "").split(",")]
        items = [item.strip() for item in items if item.strip()]
        if required and not items:
            raise RequestFormatError(f"{self._section.label}: field '{key}' needs at least one item")
        return items

    def hours(self, key: str = "hours") -> int | None:
        value = self.optional_text(key)
        if value is None:
            return None
        match = re.fullmatch(r"(\d+)\s*(h|horas|hours)?", value.lower())
        if not match:
            raise RequestFormatError(f"{self._section.label}: '{key}' must be a whole number of hours")
        return int(match.group(1))

    def certificate(self, default_folder: str) -> CertificateAttachment | None:
        source = self.optional_text("certificate")
        if source is None:
            return None
        path = Path(source.strip("\"'"))
        if not path.is_absolute():
            path = self._section.base_dir / path
        return CertificateAttachment(str(path), self.optional_text("folder") or default_folder)


def provider_folder(title: str) -> str:
    """'Docker Mastery — Udemy' -> 'Udemy' (matches the existing /certificados layout)."""
    return title.rsplit("—", 1)[1].strip() if "—" in title else "General"


_TITLE = {"titulo": "title", "title": "title", "nombre": "title"}
_CERT = {"certificado": "certificate", "certificate": "certificate", "archivo": "certificate",
         "carpeta": "folder", "folder": "folder"}
_HOURS = {"horas": "hours", "hours": "hours", "duracion": "hours"}


class SectionBuilder(ABC):
    names: tuple[str, ...] = ()
    aliases: dict[str, str] = {}

    def build(self, section: RawSection) -> CurriculumChange:
        return self._build(SectionReader(section, self.aliases))

    @abstractmethod
    def _build(self, read: SectionReader) -> CurriculumChange: ...


class CourseSection(SectionBuilder):
    names = ("curso", "course")
    aliases = {**_TITLE, **_CERT, **_HOURS, "categoria": "category", "category": "category"}

    def _build(self, read: SectionReader) -> CurriculumChange:
        title = read.text("title")
        return AddCourse(title, read.text("category"), read.hours(), certificate=read.certificate(provider_folder(title)))


class LearningPathSection(SectionBuilder):
    names = ("ruta de aprendizaje", "ruta", "learning path")
    aliases = {**_TITLE, **_CERT, **_HOURS}

    def _build(self, read: SectionReader) -> CurriculumChange:
        title = read.text("title")
        return AddLearningPath(title, read.hours(), certificate=read.certificate(provider_folder(title)))


class OfficialCertificationSection(SectionBuilder):
    names = ("certificacion oficial", "certificacion", "certification")
    aliases = {**_TITLE, **_CERT, "emisor": "issuer", "issuer": "issuer", "entidad": "issuer",
               "icono": "icon", "icon": "icon", "color": "color"}

    def _build(self, read: SectionReader) -> CurriculumChange:
        issuer = read.text("issuer")
        change = AddOfficialCertification(read.text("title"), issuer, certificate=read.certificate(issuer))
        change.icon = read.optional_text("icon") or change.icon
        change.color = read.optional_text("color") or change.color
        return change


class ExperienceSection(SectionBuilder):
    names = ("experiencia", "experience")
    aliases = {"empresa": "company", "company": "company", "cargo": "role", "rol": "role", "role": "role",
               "periodo": "period", "period": "period", "tecnologias": "technologies",
               "technologies": "technologies", "logros": "bullets", "responsabilidades": "bullets",
               "bullets": "bullets"}

    def _build(self, read: SectionReader) -> CurriculumChange:
        return AddExperience(
            Experience(
                company=read.text("company"),
                role=read.text("role"),
                period=read.text("period"),
                bullets=read.items("bullets"),
                technologies=read.items("technologies", required=False),
            )
        )


class EducationSection(SectionBuilder):
    names = ("educacion", "education", "estudio")
    aliases = {**_TITLE, "institucion": "institution", "institution": "institution",
               "ano": "year", "anio": "year", "year": "year"}

    def _build(self, read: SectionReader) -> CurriculumChange:
        return AddEducation(Education(read.text("title"), read.text("institution"), read.text("year")))


class SkillsSection(SectionBuilder):
    names = ("habilidades", "competencias", "skills")
    aliases = {"categoria": "category", "category": "category", "agregar": "items", "items": "items",
               "habilidades": "items"}

    def _build(self, read: SectionReader) -> CurriculumChange:
        return AddSkillItems(read.text("category"), read.items("items"))


class LanguageSection(SectionBuilder):
    names = ("idioma", "language")
    aliases = {"idioma": "lang", "language": "lang", "nivel": "level", "level": "level"}

    def _build(self, read: SectionReader) -> CurriculumChange:
        return SetLanguage(read.text("lang"), read.text("level"))


class ProfileSection(SectionBuilder):
    names = ("perfil", "perfil profesional", "profile")
    aliases = {"texto": "text", "text": "text"}

    def _build(self, read: SectionReader) -> CurriculumChange:
        return UpdateProfile(read.text("text"))


class PersonalFieldSection(SectionBuilder):
    names = ("dato personal", "datos personales", "contacto", "personal")
    aliases = {"campo": "field", "field": "field", "valor": "value", "value": "value"}
    fields = {"nombre": "name", "name": "name", "titulo": "title", "title": "title", "email": "email",
              "correo": "email", "telefono 1": "phone1", "telefono1": "phone1", "phone1": "phone1",
              "telefono 2": "phone2", "telefono2": "phone2", "phone2": "phone2", "ubicacion": "location",
              "location": "location", "linkedin": "linkedin", "github": "github", "portafolio": "portfolio",
              "portfolio": "portfolio", "fecha de nacimiento": "birth_date", "birth date": "birth_date"}

    def _build(self, read: SectionReader) -> CurriculumChange:
        requested = read.text("field")
        field_name = self.fields.get(normalize(requested))
        if field_name is None:
            raise RequestFormatError(f"Unknown personal field '{requested}'. Allowed: {', '.join(self.fields)}")
        return UpdatePersonalField(field_name, read.text("value"))


class RemoveTrainingSection(SectionBuilder):
    names = ("eliminar", "eliminar formacion", "eliminar curso", "remove")
    aliases = dict(_TITLE)

    def _build(self, read: SectionReader) -> CurriculumChange:
        return RemoveTraining(read.text("title"))


DEFAULT_SECTIONS: tuple[SectionBuilder, ...] = (
    CourseSection(),
    LearningPathSection(),
    OfficialCertificationSection(),
    ExperienceSection(),
    EducationSection(),
    SkillsSection(),
    LanguageSection(),
    ProfileSection(),
    PersonalFieldSection(),
    RemoveTrainingSection(),
)
