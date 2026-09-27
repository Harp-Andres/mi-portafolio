from __future__ import annotations

from pathlib import Path

import pytest

from app.domain.changes import (
    AddCourse,
    AddEducation,
    AddExperience,
    AddLearningPath,
    AddOfficialCertification,
    AddSkillItems,
    CertificateAttachment,
    RemoveTraining,
    SetLanguage,
    UpdatePersonalField,
    UpdateProfile,
)
from app.infrastructure.requests.sections import RequestFormatError
from app.infrastructure.requests.text_request_parser import TextChangeRequestParser

FULL_REQUEST = """# Actualización HV septiembre
Texto libre fuera de secciones: se ignora.
<!-- comentario
## Curso
- titulo: ignorado
-->

## Curso
- Título: Docker Mastery — Udemy
- Categoría: DevOps & Cloud
- horas: 14h
- certificado: certs/docker.pdf

## Ruta de aprendizaje
- titulo: Azure Fundamentals — Microsoft Learn
- horas: 6

## Certificación oficial
- titulo: AZ-900
- emisor: Microsoft
- icono: ☁️

## Experiencia
- empresa: ACME
- cargo: QA Lead
- periodo: 2026 – Actualidad
- tecnologias: Playwright, k6
- logros:
  - Built the framework: from zero
  - Cut regression time by 40%

## Educación
- titulo: Especialización en IA
- institucion: UNAD
- año: 2027

## Habilidades
- categoria: Performance
- agregar: k6, JMeter

## Idioma
- idioma: Inglés
- nivel: B2

## Perfil
- texto: SDET con experiencia
  en automatización.

## Dato personal
- campo: Teléfono 2
- valor: +57 300 000 0000

## Eliminar
- titulo: Old course — Udemy
"""


def parse(tmp_path: Path, text: str, name: str = "request.md"):
    request = tmp_path / name
    request.write_text(text, encoding="utf-8")
    return TextChangeRequestParser().parse(request)


def test_full_request_maps_every_section_to_a_domain_change(tmp_path):
    changes = parse(tmp_path, FULL_REQUEST)
    assert [type(c) for c in changes] == [
        AddCourse, AddLearningPath, AddOfficialCertification, AddExperience, AddEducation,
        AddSkillItems, SetLanguage, UpdateProfile, UpdatePersonalField, RemoveTraining,
    ]
    course = changes[0]
    assert (course.title, course.category, course.hours) == ("Docker Mastery — Udemy", "DevOps & Cloud", 14)
    assert course.certificate == CertificateAttachment(str(tmp_path / "certs" / "docker.pdf"), "Udemy")
    assert changes[2].icon == "☁️" and changes[2].certificate is None
    experience = changes[3].experience
    assert experience.bullets == ["Built the framework: from zero", "Cut regression time by 40%"]
    assert experience.technologies == ["Playwright", "k6"]
    assert changes[5].items == ["k6", "JMeter"]
    assert changes[7].profile == "SDET con experiencia en automatización."
    assert (changes[8].field_name, changes[8].value) == ("phone2", "+57 300 000 0000")


def test_plain_text_requests_use_bracket_sections(tmp_path):
    changes = parse(tmp_path, "[Curso]\ntitulo: K6 — Udemy\ncategoria: QA\n", name="pedido.txt")
    assert changes == [AddCourse("K6 — Udemy", "QA")]


def test_absolute_certificate_path_and_explicit_folder(tmp_path):
    source = tmp_path / "elsewhere" / "cert.jpg"
    changes = parse(tmp_path, f"## Curso\n- titulo: X\n- categoria: QA\n- certificado: \"{source}\"\n- carpeta: Docker/Udemy\n")
    assert changes[0].certificate == CertificateAttachment(str(source), "Docker/Udemy")


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("## Vacaciones\n- dias: 3\n", "Unknown section"),
        ("## Curso\n- titulo: X\n- categoria: QA\n- precio: 3\n", "unknown field 'precio'"),
        ("## Curso\n- titulo: X\n", "field 'category' is required"),
        ("## Curso\n- titulo: X\n- categoria: QA\n- horas: muchas\n", "whole number of hours"),
        ("## Dato personal\n- campo: salario\n- valor: 1\n", "Unknown personal field"),
    ],
)
def test_invalid_requests_explain_what_is_wrong(tmp_path, text, message):
    with pytest.raises(RequestFormatError, match=message):
        parse(tmp_path, text)


def test_supported_suffixes():
    parser = TextChangeRequestParser()
    assert parser.supports(Path("a.md")) and parser.supports(Path("a.TXT"))
    assert not parser.supports(Path("a.json"))
