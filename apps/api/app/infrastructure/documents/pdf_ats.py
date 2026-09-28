"""ATS PDF: one column, plain text order and no graphics that parsers read as content."""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import BaseDocTemplate, Flowable, HRFlowable, Paragraph, SimpleDocTemplate, Spacer

from app.infrastructure.documents.content import DocumentContent
from app.infrastructure.documents.pdf_renderer import PdfCurriculumRenderer
from app.infrastructure.documents.theme import ACCENT_HEX, MUTED_HEX, PRIMARY_HEX, TEXT_HEX

PRIMARY = HexColor(f"#{PRIMARY_HEX}")
ACCENT = HexColor(f"#{ACCENT_HEX}")
TEXT = HexColor(f"#{TEXT_HEX}")
MUTED = HexColor(f"#{MUTED_HEX}")


def _styles() -> dict[str, ParagraphStyle]:
    normal = getSampleStyleSheet()["Normal"]

    def style(name: str, **kwargs) -> ParagraphStyle:
        return ParagraphStyle(name, parent=normal, **kwargs)

    return {
        "name": style("CVName", fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=PRIMARY, alignment=TA_CENTER, spaceAfter=4),
        "title": style("CVTitle", fontSize=9, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=6, leading=12),
        "contact": style("CVContact", fontSize=8, textColor=TEXT, alignment=TA_CENTER, spaceAfter=2, leading=11),
        "section": style("CVSection", fontName="Helvetica-Bold", fontSize=11, textColor=PRIMARY, spaceBefore=10, spaceAfter=2, leading=14, keepWithNext=1),
        "subsection": style("CVSubSection", fontName="Helvetica-Bold", fontSize=10, textColor=ACCENT, spaceBefore=6, spaceAfter=3, keepWithNext=1),
        "body": style("CVBody", fontSize=8.5, textColor=TEXT, alignment=TA_JUSTIFY, leading=11, spaceAfter=4),
        "kv": style("CVKeyValue", fontSize=8.5, textColor=TEXT, leading=11, spaceAfter=2),
        "bullet": style("CVBullet", fontSize=8.5, textColor=TEXT, leftIndent=12, leading=11, spaceAfter=1),
        "job": style("CVJob", fontName="Helvetica-Bold", fontSize=9.5, textColor=PRIMARY, spaceBefore=6, spaceAfter=1, keepWithNext=1),
        "edu": style("CVEdu", fontSize=9, textColor=TEXT, spaceBefore=3, spaceAfter=2),
        "cat": style("CVCat", fontName="Helvetica-Bold", fontSize=8.5, textColor=PRIMARY, spaceBefore=4, spaceAfter=1, keepWithNext=1),
    }


class AtsPdfRenderer(PdfCurriculumRenderer):
    label = "ATS"

    def __init__(self, output_path: Path, variant: str = "ats") -> None:
        super().__init__(output_path, variant)
        self._s = _styles()

    def _document(self, path: Path, content: DocumentContent, metadata: dict[str, str]) -> BaseDocTemplate:
        return SimpleDocTemplate(
            str(path),
            pagesize=letter,
            leftMargin=0.7 * inch,
            rightMargin=0.7 * inch,
            topMargin=0.55 * inch,
            bottomMargin=0.55 * inch,
            **metadata,
        )

    def _story(self, c: DocumentContent) -> list[Flowable]:
        s = self._s
        story: list[Flowable] = [
            Paragraph(escape(c.name), s["name"]),
            Paragraph(escape(c.title), s["title"]),
            *(Paragraph(escape(line), s["contact"]) for line in c.contact_lines),
            Paragraph(f'Portafolio: <font color="#{ACCENT_HEX}">{escape(c.portfolio)}</font>', s["contact"]),
            Spacer(1, 4),
            *self._section("Perfil Profesional"),
            Paragraph(escape(c.profile), s["body"]),
            *self._section("Competencias Técnicas"),
        ]
        story += [Paragraph(f"{self._label(category)} {escape(items)}", s["kv"]) for category, items in c.skills]

        story += self._section("Experiencia Profesional")
        for exp in c.experience:
            heading = f"{escape(exp.company)}  —  {escape(exp.role)}"
            period = f'<font name="Helvetica-Oblique" color="#{MUTED_HEX}">{escape(exp.period)}</font>'
            story.append(Paragraph(f"{heading}&nbsp;&nbsp;|&nbsp;&nbsp;{period}", s["job"]))
            story += [Paragraph(f"- {escape(bullet)}", s["bullet"]) for bullet in exp.bullets]

        story += self._section("Educación")
        story += [
            Paragraph(f'<b><font color="#{PRIMARY_HEX}">{escape(degree)}</font></b>  —  {escape(inst)}  ({escape(year)})', s["edu"])
            for degree, inst, year in c.education
        ]

        story += self._section("Idiomas")
        story += [Paragraph(f"{self._label(lang)} {escape(level)}", s["kv"]) for lang, level in c.languages]

        story += self._section("Certificaciones & Formación")
        story.append(Paragraph("Certificaciones Oficiales", s["subsection"]))
        story += [Paragraph(f"- {escape(line)}", s["bullet"]) for line in c.official_certifications]
        story.append(Paragraph("Rutas de Aprendizaje", s["subsection"]))
        story += [Paragraph(f"- {escape(line)}", s["bullet"]) for line in c.learning_paths]
        story.append(Paragraph("Cursos de Formación", s["subsection"]))
        for category, lines in c.courses_by_category:
            story.append(Paragraph(escape(category), s["cat"]))
            story += [Paragraph(f"- {escape(line)}", s["bullet"]) for line in lines]
        return story

    def _section(self, title: str) -> list[Flowable]:
        heading = Paragraph(escape(title.upper()), self._s["section"])
        rule = HRFlowable(width="100%", thickness=0.8, color=ACCENT, spaceBefore=1, spaceAfter=5)
        rule.keepWithNext = 1
        return [heading, rule]

    @staticmethod
    def _label(text: str) -> str:
        return f'<b><font color="#{PRIMARY_HEX}">{escape(text)}:</font></b>'
