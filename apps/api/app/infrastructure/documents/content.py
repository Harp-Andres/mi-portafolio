"""What the CV documents say, independent of the format (PDF or DOCX) that lays it out."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.models import Course, CurriculumVitae, Experience

FINGERPRINT_PREFIX = "cv-fingerprint:"


def display_url(url: str) -> str:
    return url.removeprefix("https://").removeprefix("http://").removeprefix("www.")


def course_line(course: Course) -> str:
    return f"{course.title} ({course.hours}h)" if course.hours else course.title


@dataclass(frozen=True)
class DocumentContent:
    name: str
    title: str
    contact_lines: tuple[str, str]
    portfolio: str
    profile: str
    skills: list[tuple[str, str]]
    experience: list[Experience]
    education: list[tuple[str, str, str]]
    official_certifications: list[str]
    learning_paths: list[str]
    courses_by_category: list[tuple[str, list[str]]]
    languages: list[tuple[str, str]]

    @classmethod
    def from_cv(cls, cv: CurriculumVitae) -> "DocumentContent":
        p = cv.personal
        return cls(
            name=p.name,
            title=p.title,
            contact_lines=(
                f"{p.location}  |  {p.phone1}  |  {p.phone2}",
                f"{p.email}  |  {display_url(p.linkedin)}  |  {display_url(p.github)}",
            ),
            portfolio=p.portfolio,
            profile=cv.profile,
            skills=[(s.category, s.items) for s in cv.skills],
            experience=cv.experience,
            education=[(e.degree, e.institution, e.year) for e in cv.education],
            official_certifications=[f"{c.title} — {c.issuer}" for c in cv.official_certifications],
            learning_paths=[course_line(c) for c in cv.learning_paths],
            courses_by_category=[
                (category, [course_line(c) for c in courses]) for category, courses in cv.courses_by_category.items()
            ],
            languages=[(lang.lang, lang.level) for lang in cv.languages],
        )
