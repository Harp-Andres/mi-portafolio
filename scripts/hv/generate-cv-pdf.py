#!/usr/bin/env python3
"""
Generate ATS + Visual CV documents (DOCX + PDF) for MiPortafolio.

Data must stay in sync with apps/web/src/utils/cv-data.ts
Usage: python3 scripts/hv/generate-cv-pdf.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PUBLIC = REPO_ROOT / "apps/web/public/cv"
OUTPUT_HV = REPO_ROOT / "Hoja De Vida"

PRIMARY = HexColor("#1F4E79")
ACCENT = HexColor("#2E75B6")
TEXT = HexColor("#1A1A1A")
MUTED = HexColor("#555555")
LIGHT = HexColor("#F3F7FB")

PRIMARY_RGB = RGBColor(0x1F, 0x4E, 0x79)
ACCENT_RGB = RGBColor(0x2E, 0x75, 0xB6)
TEXT_RGB = RGBColor(0x1A, 0x1A, 0x1A)

DATA = {
    "name": "ANDRES RODRIGUEZ PISA",
    "title": (
        "SDET | Senior QA Automation Engineer | API · Backend · Mobile · Web | "
        "Entornos DevOps | IA aplicada a QA"
    ),
    "location": "Bogotá, Colombia",
    "phone1": "(+57) 320 324 5988",
    "phone2": "(+57) 301 211 9295",
    "email": "andresrdrgzps05@gmail.com",
    "linkedin": "linkedin.com/in/andresrodriguezpisa-qa/",
    "github": "github.com/Harp-Andres",
    "portfolio": "https://harp-andres.github.io/mi-portafolio/",
    "profile": (
        "Ingeniero de Sistemas especializado en aseguramiento de calidad de software, con "
        "expertise en arquitectura de frameworks de automatización multiplataforma (Web, API, Mobile) "
        "y prácticas DevOps de clase empresarial. Sólida experiencia en diseño e implementación de "
        "estrategias QA con patrones avanzados (Screenplay, POM), CI/CD (GitHub Actions, GitLab CI, "
        "Jenkins, Azure DevOps), ecosistema Azure (Pipelines YAML, ACR, Blob Storage, Docker) y "
        "validación de servicios REST/SOAP con trazabilidad de calidad. Liderazgo técnico demostrado "
        "en estandarización de prácticas QA, gobierno de automatización, arquitectura de frameworks "
        "mantenibles bajo principios SOLID, y capacitación continua de equipos. Activamente integro "
        "herramientas de IA (GitHub Copilot, MCP Playwright) para optimizar diseño de escenarios, "
        "refactorización y cobertura de pruebas. Enfoque senior en calidad continua, automatización "
        "inteligente, entrega de valor medible y cultura DevOps."
    ),
    "skills": [
        {"cat": "Mobile Automation", "items": "Appium, Appium Server, Appium Inspector, Android/iOS, ADB"},
        {"cat": "Web Automation", "items": "Selenium WebDriver, Playwright, Cypress, Serenity BDD, HTML, CSS"},
        {
            "cat": "API / Backend Testing",
            "items": "REST Assured, Karate, Postman, SoapUI, Swagger, validación de contratos, pruebas de integración",
        },
        {"cat": "Performance", "items": "JMeter, Gatling (básico)"},
        {
            "cat": "BDD / Frameworks",
            "items": "Cucumber, Reqnroll (.NET), Serenity BDD, JUnit, TestNG, Katalon Studio",
        },
        {
            "cat": "Arquitectura / Patrones",
            "items": "Screenplay, Page Object Model (POM), POO, DTO, Entities, IA & Productividad",
        },
        {
            "cat": "CI/CD & DevOps",
            "items": "GitHub Actions, GitLab CI/CD, Jenkins, Azure DevOps (YAML, Release, Repos, Boards), Docker, Git, SonarQube",
        },
        {"cat": "Cloud & Plataformas", "items": "BrowserStack, AWS Device Farm, Sauce Labs"},
        {
            "cat": "Azure (Contenedores & Kubernetes)",
            "items": "Azure Storage, Azure Kubernetes Service (AKS), Azure Container Registry (ACR), Docker, Kubernetes",
        },
        {"cat": "Lenguajes", "items": "Java, JavaScript, TypeScript, C#, SQL"},
        {"cat": "Build Tools", "items": "Gradle, Maven, Node.js, dotenv"},
        {"cat": "Reporting", "items": "Allure Report, Cucumber HTML, GitHub Pages Reports Hub"},
        {"cat": "Bases de Datos", "items": "SQL Server, MySQL, Oracle, PostgreSQL, MongoDB"},
        {
            "cat": "Gestión / Colaboración",
            "items": "Jira, Kanban, Azure Boards, liderazgo técnico, capacitación",
        },
        {
            "cat": "IA & Productividad",
            "items": "GitHub Copilot, MCP Playwright, MCP AppMod, prompting avanzado",
        },
        {"cat": "Scripting / Consola", "items": "PowerShell, Bash, CMD"},
        {
            "cat": "Virtualización",
            "items": "VirtualBox, VMware, Linux, WPS Office, Microsoft Office, IntelliJ IDEA, VS Code",
        },
    ],
    "experience": [
        {
            "company": "GFT Technologies",
            "role": "Test Automation Analyst III",
            "period": "Feb 2026 – Actualidad",
            "bullets": [
                "Lidero la estrategia de automatización QA en entornos CI/CD para pruebas de servicios y front-end.",
                "Diseño y ejecuto pruebas de performance para validar estabilidad y comportamiento bajo carga.",
                "Gestiono DoD, Test Plan y trazabilidad de calidad con cobertura de criterios de aceptación.",
                "Implemento pruebas de aceptación con Karate y automatización web con Serenity.",
                "Desarrollo automatizaciones inteligentes con IA integrada para auto-curación de tests.",
            ],
        },
        {
            "company": "Bizagi Latam SAS",
            "role": "Senior QA Engineer L1",
            "period": "Ago 2025 – Dic 2025",
            "bullets": [
                "Diseñé e implementé arquitecturas de automatización para pruebas API, Web y Mobile.",
                "Implementé soluciones en Azure para optimizar tiempos de ejecución.",
                "Establecí estándares de calidad técnica y patrones de diseño (Screenplay, POM).",
                "Diseñé soluciones con IA para validación visual y auto-curación de tests.",
                "Lideré capacitación QA y revisión de código con enfoque en mantenibilidad.",
            ],
        },
        {
            "company": "Tata Consultancy Services (TCS)",
            "role": "Domain Consultant – QA Automation",
            "period": "Dic 2024 – Ago 2025",
            "bullets": [
                "Orquesté marcos de automatización QA alineados a pipelines CI/CD corporativos.",
                "Analicé y reestructuré soluciones de automatización de alta complejidad.",
                "Mejoré mantenibilidad mediante estandarización técnica y principios SOLID.",
                "Administré pipelines en YAML y Azure DevOps alineados a estándares corporativos.",
                "Brindé capacitación continua al equipo QA para elevar madurez técnica.",
            ],
        },
        {
            "company": "Banco de Occidente",
            "role": "QA Automation Engineer",
            "period": "Abr 2023 – Dic 2024",
            "bullets": [
                "Diseñé estrategias de pruebas automatizadas multiplataforma (Web, API, Mobile) en entornos bancarios.",
                "Implementé pipelines CI/CD con GitHub Actions, GitLab CI y Azure DevOps.",
                "Optimicé flujos de trabajo QA y fortalecí procesos de validación funcional.",
                "Capacité continuamente al equipo QA en herramientas y buenas prácticas.",
            ],
        },
    ],
    "education": [
        {
            "title": "Ingeniero de Sistemas",
            "inst": "Universidad Nacional Abierta y a Distancia (UNAD)",
            "year": "2024",
        },
        {
            "title": "Tecnólogo en Gestión de Redes de Datos",
            "inst": "SENA",
            "year": "2018",
        },
    ],
    "officialCertifications": [
        {"title": "Linux Essentials", "issuer": "LPI"},
        {"title": "Scrum Practitioner", "issuer": "CertMind"},
    ],
    "learningPaths": [
        {"title": "JavaScript — Cymetria Group", "hours": 40},
        {
            "title": "Programa Oracle Next Education (7 formaciones) — Oracle + Alura",
            "hours": 240,
        },
    ],
    "coursesByCategory": {
        "DevOps & Cloud": [
            {
                "title": "DevOps y Cloud con Azure DevOps, App Service Pipelines y Git — Udemy",
                "hours": 21,
            },
            {"title": "Maneja Docker en 5 días: SysAdmin Linux o DevOps — Udemy", "hours": 7},
            {"title": "Docker Compose with Selenium — Udemy", "hours": 3},
            {"title": "La Guía de Jenkins: De Cero a Experto — Udemy", "hours": 32},
        ],
        "Calidad & QA": [
            {
                "title": "ISTQB Certified Tester Foundation Level (CTFL 4.0) — Udemy",
                "hours": 18,
            },
            {
                "title": "Master: Pruebas de Rendimiento con Apache JMeter — Udemy",
                "hours": 16,
            },
            {
                "title": "Introducción a Automatización de Pruebas con Puppeteer — Platzi",
                "hours": 12,
            },
        ],
        "Automatización Web & Mobile": [
            {"title": "Selenium WebDriver y Grid — Udemy", "hours": 21},
            {"title": "Selenium Essential Training — LinkedIn Learning", "hours": 5},
            {"title": "Master Class de Appium 2 con Java — Udemy", "hours": 22},
            {"title": "Configuración básica con Appium+Serenity — Udemy", "hours": 8},
            {"title": "Cypress: Master en Automatización Test QA — Udemy", "hours": 23},
            {"title": "Master: Katalon Studio Test QA Automation — Udemy", "hours": 20},
        ],
        "Playwright & API Testing": [
            {
                "title": "Automatización de Pruebas API Rest con Playwright — Udemy",
                "hours": 16,
            },
            {"title": "Curso de Playwright con JavaScript — Udemy", "hours": 19},
            {
                "title": "Dominando Playwright con TypeScript: E2E Testing moderno — Udemy",
                "hours": 21,
            },
        ],
        "IA & Productividad": [
            {"title": "AI Fluency: Framework & Foundations — Anthropic", "hours": 2},
            {"title": "Introduction to Claude Cowork — Anthropic", "hours": 1},
            {"title": "Claude 101 — Anthropic", "hours": 1},
            {
                "title": "Escriba indicaciones eficaces para lograr resultados óptimos — Microsoft",
                "hours": 3,
            },
            {"title": "Introducción a Microsoft Copilot Studio — Microsoft", "hours": 2},
            {
                "title": "Introducción a Microsoft 365 Copilot Chat (básico) — Microsoft",
                "hours": 2,
            },
        ],
    },
    "languages": [
        {"lang": "Español", "level": "Nativo"},
        {"lang": "Inglés", "level": "B1 (en progreso)"},
    ],
}


def format_course(course: dict) -> str:
    hours = course.get("hours")
    return f'{course["title"]} ({hours}h)' if hours else course["title"]


# ───────────────────────────── PDF ─────────────────────────────


def build_styles():
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "CVName",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=PRIMARY,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "title": ParagraphStyle(
            "CVTitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            textColor=ACCENT,
            alignment=TA_CENTER,
            spaceAfter=4,
            leading=12,
        ),
        "contact": ParagraphStyle(
            "CVContact",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            textColor=TEXT,
            alignment=TA_CENTER,
            spaceAfter=2,
            leading=10,
        ),
        "section": ParagraphStyle(
            "CVSection",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=PRIMARY,
            spaceBefore=10,
            spaceAfter=4,
            leading=14,
        ),
        "subsection": ParagraphStyle(
            "CVSubSection",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=ACCENT,
            spaceBefore=6,
            spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "CVBody",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            textColor=TEXT,
            alignment=TA_JUSTIFY,
            leading=11,
            spaceAfter=4,
        ),
        "kv": ParagraphStyle(
            "CVKeyValue",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            textColor=TEXT,
            leading=11,
            spaceAfter=2,
        ),
        "bullet": ParagraphStyle(
            "CVBullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            textColor=TEXT,
            leftIndent=12,
            leading=11,
            spaceAfter=1,
        ),
        "job": ParagraphStyle(
            "CVJob",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            textColor=PRIMARY,
            spaceBefore=6,
            spaceAfter=1,
        ),
        "period": ParagraphStyle(
            "CVPeriod",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            textColor=MUTED,
            spaceAfter=2,
        ),
        "edu": ParagraphStyle(
            "CVEdu",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            textColor=TEXT,
            spaceBefore=3,
            spaceAfter=2,
        ),
        "cat": ParagraphStyle(
            "CVCat",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            textColor=PRIMARY,
            spaceBefore=4,
            spaceAfter=1,
        ),
        "skill_cat": ParagraphStyle(
            "CVSkillCat",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=PRIMARY,
            spaceAfter=1,
        ),
        "skill_items": ParagraphStyle(
            "CVSkillItems",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            textColor=TEXT,
            leading=9,
        ),
    }


def section_rule(styles, title: str):
    return Paragraph(
        f'<font color="#1F4E79"><b>{title.upper()}</b></font>'
        f'<br/><font color="#2E75B6">{"_" * 78}</font>',
        styles["section"],
    )


def add_header(story, data, styles):
    story.append(Paragraph(data["name"], styles["name"]))
    story.append(Paragraph(data["title"], styles["title"]))
    story.append(
        Paragraph(
            f'{data["location"]}  |  {data["phone1"]}  |  {data["phone2"]}',
            styles["contact"],
        )
    )
    story.append(
        Paragraph(
            f'{data["email"]}  |  {data["linkedin"]}  |  {data["github"]}',
            styles["contact"],
        )
    )
    story.append(
        Paragraph(
            f'Portafolio: <font color="#2E75B6">{data["portfolio"]}</font>',
            styles["contact"],
        )
    )
    story.append(Spacer(1, 6))


def add_education_and_certs_pdf(story, data, styles):
    story.append(section_rule(styles, "Educación"))
    for edu in data["education"]:
        story.append(
            Paragraph(
                f'<b><font color="#1F4E79">{edu["title"]}</font></b>'
                f'  —  {edu["inst"]}  ({edu["year"]})',
                styles["edu"],
            )
        )

    story.append(section_rule(styles, "Certificaciones & Formación"))

    story.append(Paragraph("Certificaciones Oficiales", styles["subsection"]))
    for cert in data["officialCertifications"]:
        story.append(Paragraph(f'- {cert["title"]} — {cert["issuer"]}', styles["bullet"]))

    story.append(Paragraph("Rutas de Aprendizaje", styles["subsection"]))
    for course in data["learningPaths"]:
        story.append(Paragraph(f"- {format_course(course)}", styles["bullet"]))

    story.append(Paragraph("Cursos de Formación", styles["subsection"]))
    for category, courses in data["coursesByCategory"].items():
        story.append(Paragraph(category, styles["cat"]))
        for course in courses:
            story.append(Paragraph(f"- {format_course(course)}", styles["bullet"]))

    story.append(section_rule(styles, "Portafolio"))
    story.append(
        Paragraph(
            f'<b>Sitio web:</b> <font color="#2E75B6">{data["portfolio"]}</font>',
            styles["kv"],
        )
    )

    story.append(section_rule(styles, "Idiomas"))
    for lang in data["languages"]:
        story.append(
            Paragraph(
                f'<b><font color="#1F4E79">{lang["lang"]}:</font></b> {lang["level"]}',
                styles["kv"],
            )
        )


def build_ats_pdf(data, output_path: Path):
    styles = build_styles()
    story = []
    add_header(story, data, styles)

    story.append(section_rule(styles, "Perfil Profesional"))
    story.append(Paragraph(data["profile"], styles["body"]))

    story.append(section_rule(styles, "Competencias Técnicas"))
    for skill in data["skills"]:
        story.append(
            Paragraph(
                f'<b><font color="#1F4E79">{skill["cat"]}:</font></b> {skill["items"]}',
                styles["kv"],
            )
        )

    story.append(section_rule(styles, "Experiencia Profesional"))
    for exp in data["experience"]:
        story.append(
            Paragraph(
                f'{exp["company"]}  —  {exp["role"]}    '
                f'<font color="#555555"><i>{exp["period"]}</i></font>',
                styles["job"],
            )
        )
        for bullet in exp["bullets"]:
            story.append(Paragraph(f"- {bullet}", styles["bullet"]))

    add_education_and_certs_pdf(story, data, styles)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
        title=f'{data["name"]} - CV ATS',
        author=data["name"],
    )
    doc.build(story)


def build_visual_pdf(data, output_path: Path):
    """Visual CV: same content as ATS with accent styling and compact skills grid."""
    styles = build_styles()
    story = []
    add_header(story, data, styles)

    story.append(section_rule(styles, "Perfil Profesional"))
    story.append(Paragraph(data["profile"], styles["body"]))

    story.append(section_rule(styles, "Competencias Técnicas"))
    for skill in data["skills"]:
        story.append(
            Paragraph(
                f'<b><font color="#1F4E79">{skill["cat"]}:</font></b> {skill["items"]}',
                styles["kv"],
            )
        )

    story.append(section_rule(styles, "Experiencia Profesional"))
    for exp in data["experience"]:
        story.append(Paragraph(f'{exp["company"]}  —  {exp["role"]}', styles["job"]))
        story.append(Paragraph(exp["period"], styles["period"]))
        for bullet in exp["bullets"]:
            story.append(Paragraph(f"- {bullet}", styles["bullet"]))

    add_education_and_certs_pdf(story, data, styles)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        title=f'{data["name"]} - CV Visual',
        author=data["name"],
    )
    doc.build(story)


# ───────────────────────────── DOCX ─────────────────────────────


def _set_run(run, *, bold=False, size=10, color=TEXT_RGB, italic=False):
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.color.rgb = color


def _add_bottom_border(paragraph):
    p = paragraph._p
    pPr = p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "12")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "2E75B6")
    pBdr.append(bottom)
    pPr.append(pBdr)


def add_section_title_docx(doc: Document, text: str):
    p = doc.add_paragraph()
    run = p.add_run(text.upper())
    _set_run(run, bold=True, size=12, color=PRIMARY_RGB)
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    _add_bottom_border(p)


def add_subsection_docx(doc: Document, text: str):
    p = doc.add_paragraph()
    run = p.add_run(text)
    _set_run(run, bold=True, size=11, color=ACCENT_RGB)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)


def add_bullet_docx(doc: Document, text: str):
    p = doc.add_paragraph(style="List Bullet")
    run = p.add_run(text)
    _set_run(run, size=10, color=TEXT_RGB)


def add_education_and_certs_docx(doc: Document, data: dict):
    add_section_title_docx(doc, "Educación")
    for edu in data["education"]:
        p = doc.add_paragraph()
        r1 = p.add_run(edu["title"])
        _set_run(r1, bold=True, size=10.5, color=PRIMARY_RGB)
        r2 = p.add_run(f'  —  {edu["inst"]}  ({edu["year"]})')
        _set_run(r2, size=10, color=TEXT_RGB)

    add_section_title_docx(doc, "Certificaciones & Formación")

    add_subsection_docx(doc, "Certificaciones Oficiales")
    for cert in data["officialCertifications"]:
        add_bullet_docx(doc, f'{cert["title"]} — {cert["issuer"]}')

    add_subsection_docx(doc, "Rutas de Aprendizaje")
    for course in data["learningPaths"]:
        add_bullet_docx(doc, format_course(course))

    add_subsection_docx(doc, "Cursos de Formación")
    for category, courses in data["coursesByCategory"].items():
        p = doc.add_paragraph()
        run = p.add_run(category)
        _set_run(run, bold=True, size=10, color=PRIMARY_RGB)
        for course in courses:
            add_bullet_docx(doc, format_course(course))

    add_section_title_docx(doc, "Portafolio")
    p = doc.add_paragraph()
    r1 = p.add_run("Sitio web: ")
    _set_run(r1, bold=True, size=10, color=PRIMARY_RGB)
    r2 = p.add_run(data["portfolio"])
    _set_run(r2, size=10, color=ACCENT_RGB)

    add_section_title_docx(doc, "Idiomas")
    for lang in data["languages"]:
        p = doc.add_paragraph()
        r1 = p.add_run(f'{lang["lang"]}: ')
        _set_run(r1, bold=True, size=10, color=PRIMARY_RGB)
        r2 = p.add_run(lang["level"])
        _set_run(r2, size=10, color=TEXT_RGB)


def build_docx(data: dict, output_path: Path, visual: bool = False):
    doc = Document()
    for section in doc.sections:
        section.top_margin = Pt(54)
        section.bottom_margin = Pt(54)
        section.left_margin = Pt(54 if visual else 60)
        section.right_margin = Pt(54 if visual else 60)

    name = doc.add_paragraph()
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = name.add_run(data["name"])
    _set_run(r, bold=True, size=18, color=PRIMARY_RGB)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title.add_run(data["title"])
    _set_run(r, size=10, color=ACCENT_RGB)

    for line in (
        f'{data["location"]}  |  {data["phone1"]}  |  {data["phone2"]}',
        f'{data["email"]}  |  {data["linkedin"]}  |  {data["github"]}',
        f'Portafolio: {data["portfolio"]}',
    ):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(line)
        _set_run(r, size=9, color=TEXT_RGB if "Portafolio" not in line else ACCENT_RGB)

    add_section_title_docx(doc, "Perfil Profesional")
    p = doc.add_paragraph()
    r = p.add_run(data["profile"])
    _set_run(r, size=10, color=TEXT_RGB)

    add_section_title_docx(doc, "Competencias Técnicas")
    for skill in data["skills"]:
        p = doc.add_paragraph()
        r1 = p.add_run(f'{skill["cat"]}: ')
        _set_run(r1, bold=True, size=10, color=PRIMARY_RGB)
        r2 = p.add_run(skill["items"])
        _set_run(r2, size=10, color=TEXT_RGB)

    add_section_title_docx(doc, "Experiencia Profesional")
    for exp in data["experience"]:
        p = doc.add_paragraph()
        r1 = p.add_run(f'{exp["company"]}  —  {exp["role"]}')
        _set_run(r1, bold=True, size=11, color=PRIMARY_RGB)
        p2 = doc.add_paragraph()
        r2 = p2.add_run(exp["period"])
        _set_run(r2, size=9, color=MUTED if False else RGBColor(0x55, 0x55, 0x55), italic=True)
        for bullet in exp["bullets"]:
            add_bullet_docx(doc, bullet)

    add_education_and_certs_docx(doc, data)
    doc.save(str(output_path))


def write_all(data: dict):
    OUTPUT_PUBLIC.mkdir(parents=True, exist_ok=True)
    OUTPUT_HV.mkdir(parents=True, exist_ok=True)

    targets = [
        ("HV_2026_2_ATS_AndresRodriguez.pdf", lambda p: build_ats_pdf(data, p)),
        ("HV_2026_2_Visual_AndresRodriguez.pdf", lambda p: build_visual_pdf(data, p)),
        ("HV_2026_2_ATS_AndresRodriguez.docx", lambda p: build_docx(data, p, visual=False)),
        ("HV_2026_2_Visual_AndresRodriguez.docx", lambda p: build_docx(data, p, visual=True)),
    ]

    for filename, builder in targets:
        for folder in (OUTPUT_PUBLIC, OUTPUT_HV):
            path = folder / filename
            builder(path)
            print(f"✅ {path}")

    export_path = Path(__file__).with_name("cv-export-data.json")
    export_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ {export_path}")


def main():
    # Optional: override DATA from JSON (compatibility with older callers)
    if len(sys.argv) >= 2 and Path(sys.argv[1]).exists():
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    else:
        data = DATA
    write_all(data)
    print("\n🎉 CV DOCX + PDF regenerados.")


if __name__ == "__main__":
    main()
