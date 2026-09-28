"""Maps the CV aggregate to/from the JSON contract read by packages/core (see types/cv.ts)."""

from __future__ import annotations

from typing import Any

from app.domain.models import (
    Course,
    CurriculumVitae,
    Education,
    Experience,
    Language,
    OfficialCertification,
    PersonalInfo,
    SkillCategory,
)

_PERSONAL_KEYS = {
    "name": "name",
    "title": "title",
    "email": "email",
    "phone1": "phone1",
    "phone2": "phone2",
    "location": "location",
    "linkedin": "linkedin",
    "github": "github",
    "portfolio": "portfolio",
    "birth_date": "birthDate",
}


class CurriculumJsonCodec:
    def decode(self, data: dict[str, Any]) -> CurriculumVitae:
        return CurriculumVitae(
            personal=PersonalInfo(**{attr: data[key] for attr, key in _PERSONAL_KEYS.items()}),
            profile=data["profile"],
            skills=[SkillCategory(s["category"], s["items"]) for s in data["skills"]],
            experience=[
                Experience(e["company"], e["role"], e["period"], list(e["bullets"]), list(e.get("technologies", [])))
                for e in data["experience"]
            ],
            education=[Education(e["degree"], e["institution"], e["year"]) for e in data["education"]],
            official_certifications=[
                OfficialCertification(
                    c["title"],
                    c["issuer"],
                    c.get("color", OfficialCertification.DEFAULT_COLOR),
                    c.get("icon", OfficialCertification.DEFAULT_ICON),
                    c.get("filePath"),
                )
                for c in data["officialCertifications"]
            ],
            courses_by_category={
                category: [self._decode_course(c) for c in courses]
                for category, courses in data["certificatesByCategory"].items()
            },
            learning_paths=[self._decode_course(c) for c in data["learningPathsCertifications"]],
            languages=[Language(lang["lang"], lang["level"]) for lang in data["languages"]],
        )

    def encode(self, cv: CurriculumVitae) -> dict[str, Any]:
        data: dict[str, Any] = {key: getattr(cv.personal, attr) for attr, key in _PERSONAL_KEYS.items()}
        data["profile"] = cv.profile
        data["skills"] = [{"category": s.category, "items": s.items} for s in cv.skills]
        data["experience"] = [
            {
                "company": e.company,
                "role": e.role,
                "period": e.period,
                "technologies": e.technologies,
                "bullets": e.bullets,
            }
            for e in cv.experience
        ]
        data["education"] = [
            {"degree": e.degree, "institution": e.institution, "year": e.year} for e in cv.education
        ]
        data["officialCertifications"] = [
            {"title": c.title, "issuer": c.issuer, "color": c.color, "icon": c.icon, "filePath": c.file_path}
            for c in cv.official_certifications
        ]
        data["certificatesByCategory"] = {
            category: [self._encode_course(c) for c in courses]
            for category, courses in cv.courses_by_category.items()
        }
        data["learningPathsCertifications"] = [self._encode_course(c) for c in cv.learning_paths]
        data["languages"] = [{"lang": lang.lang, "level": lang.level} for lang in cv.languages]
        return data

    @staticmethod
    def _decode_course(data: dict[str, Any]) -> Course:
        return Course(data["title"], data.get("hours"), data.get("filePath"))

    @staticmethod
    def _encode_course(course: Course) -> dict[str, Any]:
        encoded: dict[str, Any] = {"title": course.title, "filePath": course.file_path}
        if course.hours is not None:
            encoded["hours"] = course.hours
        return encoded
