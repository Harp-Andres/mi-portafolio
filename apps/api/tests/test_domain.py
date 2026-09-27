from __future__ import annotations

import copy

import pytest

from app.domain.changes import AddCourse, AddSkillItems, RemoveTraining, SetLanguage, UpdatePersonalField
from app.domain.errors import DuplicateEntryError, EntryNotFoundError, InvalidCurriculumError
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
from app.domain.validation import CurriculumValidator


@pytest.fixture
def cv() -> CurriculumVitae:
    return CurriculumVitae(
        personal=PersonalInfo("Ana", "QA", "a@b.co", "1", "2", "Bogotá", "in/ana", "gh/ana", "https://p", "1990-01-01"),
        profile="Profile",
        skills=[SkillCategory("Testing", "Playwright, Cypress")],
        experience=[Experience("ACME", "QA", "2024", ["Did things"])],
        education=[Education("Eng", "UNAD", "2024")],
        official_certifications=[OfficialCertification("ISTQB", "ISTQB")],
        courses_by_category={"QA": [Course("Docker — Udemy", 10)]},
        learning_paths=[Course("JS — Cymetria", 40)],
        languages=[Language("Español", "Nativo")],
    )


def test_add_course_creates_category_and_rejects_duplicates_across_all_training(cv):
    AddCourse("K8s — Udemy", "DevOps", 8).apply(cv)
    assert cv.courses_by_category["DevOps"] == [Course("K8s — Udemy", 8)]
    with pytest.raises(DuplicateEntryError):
        AddCourse("istqb", "QA").apply(cv)


def test_remove_training_drops_empty_categories(cv):
    RemoveTraining("docker — udemy").apply(cv)
    assert "QA" not in cv.courses_by_category
    with pytest.raises(EntryNotFoundError):
        RemoveTraining("missing").apply(cv)


def test_skill_items_are_merged_without_duplicates(cv):
    AddSkillItems("testing", ["cypress", "k6"]).apply(cv)
    AddSkillItems("Cloud", ["Azure"]).apply(cv)
    assert cv.skills[0].items == "Playwright, Cypress, k6"
    assert cv.skills[1] == SkillCategory("Cloud", "Azure")


def test_language_is_updated_in_place_or_added(cv):
    SetLanguage("español", "Nativo (C2)").apply(cv)
    SetLanguage("Inglés", "B2").apply(cv)
    assert [(lang.lang, lang.level) for lang in cv.languages] == [("Español", "Nativo (C2)"), ("Inglés", "B2")]


def test_personal_field_must_exist(cv):
    UpdatePersonalField("title", "SDET").apply(cv)
    assert cv.personal.title == "SDET"
    with pytest.raises(EntryNotFoundError):
        UpdatePersonalField("salary", "1").apply(cv)


def test_fingerprint_changes_only_when_content_changes(cv):
    same = copy.deepcopy(cv)
    assert cv.fingerprint() == same.fingerprint()
    AddSkillItems("Testing", ["k6"]).apply(same)
    assert cv.fingerprint() != same.fingerprint()


def test_validator_reports_every_problem(cv):
    cv.profile = " "
    cv.languages = []
    cv.learning_paths.append(Course("ISTQB"))
    problems = CurriculumValidator().problems(cv)
    assert "profile is empty" in problems
    assert "languages must not be empty" in problems
    assert "'ISTQB' is duplicated" in problems
    with pytest.raises(InvalidCurriculumError):
        CurriculumValidator().ensure_valid(cv)
