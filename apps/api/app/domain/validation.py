"""Business rules a CV must satisfy before documents are rendered."""

from __future__ import annotations

from app.domain.errors import InvalidCurriculumError
from app.domain.models import CurriculumVitae, PersonalInfo


class CurriculumValidator:
    def problems(self, cv: CurriculumVitae) -> list[str]:
        problems: list[str] = []
        for name in PersonalInfo.editable_fields():
            if not str(getattr(cv.personal, name)).strip():
                problems.append(f"personal '{name}' is empty")
        if not cv.profile.strip():
            problems.append("profile is empty")

        for label, collection in (
            ("skills", cv.skills),
            ("experience", cv.experience),
            ("education", cv.education),
            ("official certifications", cv.official_certifications),
            ("learning paths", cv.learning_paths),
            ("languages", cv.languages),
        ):
            if not collection:
                problems.append(f"{label} must not be empty")
        if not any(cv.courses_by_category.values()):
            problems.append("courses must not be empty")

        for exp in cv.experience:
            if not (exp.company and exp.role and exp.period and exp.bullets):
                problems.append(f"experience '{exp.role or exp.company}' needs company, role, period and bullets")

        seen: set[str] = set()
        for title in cv.training_titles():
            key = title.casefold()
            if key in seen:
                problems.append(f"'{title}' is duplicated")
            seen.add(key)

        courses = [*cv.learning_paths, *(c for group in cv.courses_by_category.values() for c in group)]
        for course in courses:
            if course.hours is not None and course.hours < 0:
                problems.append(f"'{course.title}': hours must be >= 0")
        return problems

    def ensure_valid(self, cv: CurriculumVitae) -> None:
        problems = self.problems(cv)
        if problems:
            raise InvalidCurriculumError(problems)
