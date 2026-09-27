"""PDF layouts of the CV (ATS and Visual) with ReportLab."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Flowable, Paragraph, SimpleDocTemplate, Spacer

from app.application.ports import DocumentRenderer, RenderedDocument
from app.domain.models import CurriculumVitae
from app.infrastructure.documents.content import FINGERPRINT_PREFIX, DocumentContent
from app.infrastructure.documents.theme import ACCENT_HEX, MUTED_HEX, PRIMARY_HEX, TEXT_HEX

PRIMARY = HexColor(f"#{PRIMARY_HEX}")
ACCENT = HexColor(f"#{ACCENT_HEX}")
TEXT = HexColor(f"#{TEXT_HEX}")
MUTED = HexColor(f"#{MUTED_HEX}")


@dataclass(frozen=True)
class PdfLayout:
    """What changes between the ATS and the Visual PDF."""

    margin_x: float
    margin_y: float
    period_on_own_line: bool


ATS_PDF = PdfLayout(margin_x=0.7 * inch, margin_y=0.55 * inch, period_on_own_line=False)
VISUAL_PDF = PdfLayout(margin_x=0.6 * inch, margin_y=0.5 * inch, period_on_own_line=True)


def _styles() -> dict[str, ParagraphStyle]:
    normal = getSampleStyleSheet()["Normal"]

    def style(name: str, **kwargs) -> ParagraphStyle:
        return ParagraphStyle(name, parent=normal, **kwargs)

    return {
        "name": style("CVName", fontName="Helvetica-Bold", fontSize=18, textColor=PRIMARY, alignment=TA_CENTER, spaceAfter=4),
        "title": style("CVTitle", fontSize=9, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=4, leading=12),
        "contact": style("CVContact", fontSize=8, textColor=TEXT, alignment=TA_CENTER, spaceAfter=2, leading=10),
        "section": style("CVSection", fontName="Helvetica-Bold", fontSize=11, textColor=PRIMARY, spaceBefore=10, spaceAfter=4, leading=14),
        "subsection": style("CVSubSection", fontName="Helvetica-Bold", fontSize=10, textColor=ACCENT, spaceBefore=6, spaceAfter=3),
        "body": style("CVBody", fontSize=8.5, textColor=TEXT, alignment=TA_JUSTIFY, leading=11, spaceAfter=4),
        "kv": style("CVKeyValue", fontSize=8.5, textColor=TEXT, leading=11, spaceAfter=2),
        "bullet": style("CVBullet", fontSize=8.5, textColor=TEXT, leftIndent=12, leading=11, spaceAfter=1),
        "job": style("CVJob", fontName="Helvetica-Bold", fontSize=9.5, textColor=PRIMARY, spaceBefore=6, spaceAfter=1),
        "period": style("CVPeriod", fontName="Helvetica-Oblique", fontSize=8, textColor=MUTED, spaceAfter=2),
        "edu": style("CVEdu", fontSize=9, textColor=TEXT, spaceBefore=3, spaceAfter=2),
        "cat": style("CVCat", fontName="Helvetica-Bold", fontSize=8.5, textColor=PRIMARY, spaceBefore=4, spaceAfter=1),
    }


class PdfCurriculumRenderer(DocumentRenderer):
    def __init__(self, output_path: Path, variant: str, layout: PdfLayout) -> None:
        self._output_path = output_path
        self._variant = variant
        self._layout = layout

    @property
    def variant(self) -> str:
        return self._variant

    @property
    def output_path(self) -> Path:
        return self._output_path

    def render(self, cv: CurriculumVitae, fingerprint: str) -> RenderedDocument:
        content = DocumentContent.from_cv(cv)
        self._output_path.parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(
            str(self._output_path),
            pagesize=letter,
            leftMargin=self._layout.margin_x,
            rightMargin=self._layout.margin_x,
            topMargin=self._layout.margin_y,
            bottomMargin=self._layout.margin_y,
            title=f"{content.name} - CV {self._variant.upper() if self._variant == 'ats' else self._variant.title()}",
            author=content.name,
            subject="Hoja de vida",
            keywords=f"{FINGERPRINT_PREFIX}{fingerprint}",
        )
        doc.build(self._story(content, _styles()))
        return RenderedDocument(self._variant, self._output_path)

    def _story(self, c: DocumentContent, s: dict[str, ParagraphStyle]) -> list[Flowable]:
        story: list[Flowable] = [
            Paragraph(escape(c.name), s["name"]),
            Paragraph(escape(c.title), s["title"]),
            *(Paragraph(escape(line), s["contact"]) for line in c.contact_lines),
            Paragraph(f'Portafolio: <font color="#{ACCENT_HEX}">{escape(c.portfolio)}</font>', s["contact"]),
            Spacer(1, 6),
            self._section("Perfil Profesional", s),
            Paragraph(escape(c.profile), s["body"]),
            self._section("Competencias Técnicas", s),
        ]
        story += [Paragraph(f"{self._label(category)} {escape(items)}", s["kv"]) for category, items in c.skills]

        story.append(self._section("Experiencia Profesional", s))
        for exp in c.experience:
            heading = f"{escape(exp.company)}  —  {escape(exp.role)}"
            if self._layout.period_on_own_line:
                story += [Paragraph(heading, s["job"]), Paragraph(escape(exp.period), s["period"])]
            else:
                story.append(Paragraph(f'{heading}    <font color="#{MUTED_HEX}"><i>{escape(exp.period)}</i></font>', s["job"]))
            story += [Paragraph(f"- {escape(bullet)}", s["bullet"]) for bullet in exp.bullets]

        story.append(self._section("Educación", s))
        story += [
            Paragraph(f'<b><font color="#{PRIMARY_HEX}">{escape(degree)}</font></b>  —  {escape(inst)}  ({escape(year)})', s["edu"])
            for degree, inst, year in c.education
        ]

        story.append(self._section("Certificaciones & Formación", s))
        story.append(Paragraph("Certificaciones Oficiales", s["subsection"]))
        story += [Paragraph(f"- {escape(line)}", s["bullet"]) for line in c.official_certifications]
        story.append(Paragraph("Rutas de Aprendizaje", s["subsection"]))
        story += [Paragraph(f"- {escape(line)}", s["bullet"]) for line in c.learning_paths]
        story.append(Paragraph("Cursos de Formación", s["subsection"]))
        for category, lines in c.courses_by_category:
            story.append(Paragraph(escape(category), s["cat"]))
            story += [Paragraph(f"- {escape(line)}", s["bullet"]) for line in lines]

        story.append(self._section("Portafolio", s))
        story.append(Paragraph(f'<b>Sitio web:</b> <font color="#{ACCENT_HEX}">{escape(c.portfolio)}</font>', s["kv"]))
        story.append(self._section("Idiomas", s))
        story += [Paragraph(f"{self._label(lang)} {escape(level)}", s["kv"]) for lang, level in c.languages]
        return story

    @staticmethod
    def _section(title: str, s: dict[str, ParagraphStyle]) -> Paragraph:
        return Paragraph(
            f'<font color="#{PRIMARY_HEX}"><b>{escape(title.upper())}</b></font>'
            f'<br/><font color="#{ACCENT_HEX}">{"_" * 78}</font>',
            s["section"],
        )

    @staticmethod
    def _label(text: str) -> str:
        return f'<b><font color="#{PRIMARY_HEX}">{escape(text)}:</font></b>'
