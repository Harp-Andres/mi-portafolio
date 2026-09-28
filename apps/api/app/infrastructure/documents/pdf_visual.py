"""Visual PDF: gradient header, skills sidebar and experience timeline, meant for people.

The two columns are one table row that ReportLab splits across pages (`splitInRow`), so the sidebar
and the main column flow side by side. Header, sidebar surface and footer are painted per page.
"""

from __future__ import annotations

from functools import partial
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    NextPageTemplate,
    PageTemplate,
    Paragraph,
    Table,
    TableStyle,
)

from app.domain.models import Experience
from app.infrastructure.documents.content import DocumentContent, display_url
from app.infrastructure.documents.pdf_renderer import PdfCurriculumRenderer
from app.infrastructure.documents.theme import (
    ACCENT_HEX,
    CHIP_HEX,
    HIGHLIGHT_HEX,
    MUTED_HEX,
    NAVY_HEX,
    ON_DARK_HEX,
    PRIMARY_HEX,
    RULE_HEX,
    SURFACE_HEX,
    TEXT_HEX,
)

PAGE_W, PAGE_H = letter
HEADER_H = 128
SIDEBAR_W = 200
SIDE_PAD = 18
GUTTER = 20
RIGHT = 36
BOTTOM = 40
TOP_LATER = 36
MAIN_W = PAGE_W - RIGHT - SIDEBAR_W
MAIN_INNER = MAIN_W - GUTTER

NAVY = HexColor(f"#{NAVY_HEX}")
PRIMARY = HexColor(f"#{PRIMARY_HEX}")
ACCENT = HexColor(f"#{ACCENT_HEX}")
HIGHLIGHT = HexColor(f"#{HIGHLIGHT_HEX}")
SURFACE = HexColor(f"#{SURFACE_HEX}")
RULE = HexColor(f"#{RULE_HEX}")
TEXT = HexColor(f"#{TEXT_HEX}")
MUTED = HexColor(f"#{MUTED_HEX}")


class SectionHeading(Flowable):
    """Uppercase section title with a short rounded accent bar underneath."""

    def __init__(self, text: str, size: float, color: Color, space_before: float) -> None:
        super().__init__()
        self._text = text.upper()
        self._size = size
        self._color = color
        self._space_before = space_before
        self.keepWithNext = 1

    def wrap(self, avail_width: float, avail_height: float) -> tuple[float, float]:
        self.width = avail_width
        self.height = self._size + 7
        return self.width, self.height

    def getSpaceBefore(self) -> float:
        return self._space_before

    def getSpaceAfter(self) -> float:
        return 6

    def draw(self) -> None:
        self.canv.setFillColor(self._color)
        self.canv.setFont("Helvetica-Bold", self._size)
        self.canv.drawString(0, 7, self._text)
        self.canv.setFillColor(ACCENT)
        self.canv.roundRect(0, 0, 24, 2.6, 1.3, stroke=0, fill=1)


def _styles() -> dict[str, ParagraphStyle]:
    normal = getSampleStyleSheet()["Normal"]

    def style(name: str, **kwargs) -> ParagraphStyle:
        return ParagraphStyle(name, parent=normal, **kwargs)

    return {
        "name": style("VName", fontName="Helvetica-Bold", fontSize=25, leading=29, textColor=white),
        "headline": style("VHeadline", fontSize=9.6, leading=12.5, textColor=HexColor(f"#{ON_DARK_HEX}")),
        "contact": style("VContact", fontSize=8, leading=11.5, textColor=white),
        "body": style("VBody", fontSize=8.8, leading=12.2, textColor=TEXT, alignment=TA_JUSTIFY),
        "side_label": style("VSideLabel", fontName="Helvetica-Bold", fontSize=7.9, leading=10, textColor=PRIMARY, spaceBefore=5, keepWithNext=1),
        "side_text": style("VSideText", fontSize=7.6, leading=10, textColor=TEXT),
        "side_muted": style("VSideMuted", fontSize=7.4, leading=9.6, textColor=MUTED),
        "side_bullet": style("VSideBullet", fontSize=7.6, leading=10, textColor=TEXT, leftIndent=8, bulletIndent=0, bulletColor=ACCENT, spaceBefore=2),
        "role": style("VRole", fontName="Helvetica-Bold", fontSize=10, leading=12.5, textColor=PRIMARY),
        "org": style("VOrg", fontSize=8.6, leading=11.5, textColor=ACCENT, spaceAfter=2),
        "bullet": style("VBullet", fontSize=8.4, leading=11, textColor=TEXT, leftIndent=9, bulletIndent=0, bulletColor=ACCENT, spaceBefore=1),
        "chips": style("VChips", fontSize=7.2, leading=12.5, textColor=PRIMARY, spaceBefore=3),
        "course_cat": style("VCourseCat", fontName="Helvetica-Bold", fontSize=8.6, leading=11, textColor=PRIMARY, spaceBefore=6, keepWithNext=1),
        "course": style("VCourse", fontSize=8, leading=10.5, textColor=TEXT, leftIndent=9, bulletIndent=0, bulletColor=ACCENT),
        "callout": style("VCallout", fontSize=8.6, leading=12, textColor=TEXT),
    }


def _link(url: str, text: str, color: str) -> str:
    return f'<a href="{escape(url)}" color="#{color}">{escape(text)}</a>'


class VisualPdfRenderer(PdfCurriculumRenderer):
    label = "Visual"

    def __init__(self, output_path: Path, variant: str = "visual") -> None:
        super().__init__(output_path, variant)
        self._s = _styles()

    # ── page template ────────────────────────────────────────

    def _document(self, path: Path, content: DocumentContent, metadata: dict[str, str]) -> BaseDocTemplate:
        document = BaseDocTemplate(str(path), pagesize=letter, **metadata)
        no_padding = {"leftPadding": 0, "rightPadding": 0, "topPadding": 0, "bottomPadding": 0}
        first_height = PAGE_H - HEADER_H - 3 - 18 - BOTTOM
        first = Frame(0, BOTTOM, PAGE_W - RIGHT, first_height, id="first", **no_padding)
        later = Frame(0, BOTTOM, PAGE_W - RIGHT, PAGE_H - TOP_LATER - BOTTOM, id="later", **no_padding)
        document.addPageTemplates([
            PageTemplate("first", [first], onPage=partial(self._paint_first_page, content)),
            PageTemplate("later", [later], onPage=partial(self._paint_later_page, content)),
        ])
        return document

    def _paint_first_page(self, content: DocumentContent, canvas: Canvas, document: BaseDocTemplate) -> None:
        header_bottom = PAGE_H - HEADER_H
        canvas.saveState()
        self._paint_sidebar(canvas, header_bottom)
        clip = canvas.beginPath()
        clip.rect(0, header_bottom, PAGE_W, HEADER_H)
        canvas.clipPath(clip, stroke=0, fill=0)
        canvas.linearGradient(0, header_bottom, PAGE_W, PAGE_H, (NAVY, PRIMARY), extend=False)
        canvas.restoreState()

        canvas.saveState()
        canvas.setFillColor(HIGHLIGHT)
        canvas.rect(0, header_bottom - 3, PAGE_W, 3, stroke=0, fill=1)
        y = PAGE_H - 24
        for paragraph in self._header(content):
            _, height = paragraph.wrap(PAGE_W - 2 * RIGHT, HEADER_H)
            y -= height
            paragraph.drawOn(canvas, RIGHT, y)
            y -= 3
        self._paint_footer(canvas, document, content)
        canvas.restoreState()

    def _paint_later_page(self, content: DocumentContent, canvas: Canvas, document: BaseDocTemplate) -> None:
        canvas.saveState()
        self._paint_sidebar(canvas, PAGE_H)
        canvas.setFillColor(NAVY)
        canvas.rect(0, PAGE_H - 8, PAGE_W, 8, stroke=0, fill=1)
        canvas.setFillColor(HIGHLIGHT)
        canvas.rect(0, PAGE_H - 10, PAGE_W, 2, stroke=0, fill=1)
        self._paint_footer(canvas, document, content)
        canvas.restoreState()

    @staticmethod
    def _paint_sidebar(canvas: Canvas, top: float) -> None:
        canvas.setFillColor(SURFACE)
        canvas.rect(0, 0, SIDEBAR_W, top, stroke=0, fill=1)
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.6)
        canvas.line(SIDEBAR_W, 0, SIDEBAR_W, top)

    @staticmethod
    def _paint_footer(canvas: Canvas, document: BaseDocTemplate, content: DocumentContent) -> None:
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(PAGE_W - RIGHT, 20, f"{content.name}  ·  Hoja de vida  ·  {document.page}")

    def _header(self, c: DocumentContent) -> list[Paragraph]:
        s, contact = self._s, c.contact
        separator = f'&nbsp;&nbsp;<font color="#{HIGHLIGHT_HEX}">|</font>&nbsp;&nbsp;'
        reach = [escape(contact.location), *(escape(phone) for phone in contact.phones), _link(f"mailto:{contact.email}", contact.email, "FFFFFF")]
        profiles = [_link(url, display_url(url), "FFFFFF") for url in (contact.linkedin, contact.github, contact.portfolio)]
        return [
            Paragraph(escape(c.name), s["name"]),
            Paragraph(escape(c.title), s["headline"]),
            Paragraph(separator.join(reach), s["contact"]),
            Paragraph(separator.join(profiles), s["contact"]),
        ]

    # ── story ────────────────────────────────────────────────

    def _story(self, c: DocumentContent) -> list[Flowable]:
        body = Table(
            [[self._sidebar(c), self._main(c)]],
            colWidths=[SIDEBAR_W, MAIN_W],
            splitInRow=1,
            style=TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (0, 0), SIDE_PAD),
                ("RIGHTPADDING", (0, 0), (0, 0), SIDE_PAD - 4),
                ("LEFTPADDING", (1, 0), (1, 0), GUTTER),
                ("RIGHTPADDING", (1, 0), (1, 0), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]),
        )
        return [NextPageTemplate("later"), body]

    def _sidebar(self, c: DocumentContent) -> list[Flowable]:
        s = self._s
        items: list[Flowable] = [SectionHeading("Competencias", 9.5, PRIMARY, 0)]
        for category, skills in c.skills:
            items += [Paragraph(escape(category), s["side_label"]), Paragraph(escape(skills), s["side_text"])]

        items.append(SectionHeading("Educación", 9.5, PRIMARY, 14))
        for degree, institution, year in c.education:
            items += [
                Paragraph(escape(degree), s["side_label"]),
                Paragraph(escape(institution), s["side_text"]),
                Paragraph(escape(year), s["side_muted"]),
            ]

        items.append(SectionHeading("Certificaciones", 9.5, PRIMARY, 14))
        items += [Paragraph(escape(line), s["side_bullet"], bulletText="•") for line in c.official_certifications]
        items.append(SectionHeading("Rutas de aprendizaje", 9.5, PRIMARY, 14))
        items += [Paragraph(escape(line), s["side_bullet"], bulletText="•") for line in c.learning_paths]

        items.append(SectionHeading("Idiomas", 9.5, PRIMARY, 14))
        items += [
            Paragraph(f'<b><font color="#{PRIMARY_HEX}">{escape(lang)}</font></b>&nbsp;&nbsp;{escape(level)}', s["side_text"])
            for lang, level in c.languages
        ]
        return items

    def _main(self, c: DocumentContent) -> list[Flowable]:
        s = self._s
        items: list[Flowable] = [
            SectionHeading("Perfil profesional", 11.5, PRIMARY, 0),
            Paragraph(escape(c.profile), s["body"]),
            SectionHeading("Experiencia profesional", 11.5, PRIMARY, 14),
        ]
        items += [self._job(exp) for exp in c.experience]

        items.append(SectionHeading("Cursos de formación", 11.5, PRIMARY, 14))
        for category, lines in c.courses_by_category:
            items.append(Paragraph(f'{escape(category)}&nbsp;&nbsp;<font color="#{MUTED_HEX}" size="7.5">({len(lines)})</font>', s["course_cat"]))
            items += [Paragraph(escape(line), s["course"], bulletText="•") for line in lines]

        items += [SectionHeading("Portafolio", 11.5, PRIMARY, 14), self._callout(c)]
        return items

    def _job(self, exp: Experience) -> Table:
        s = self._s
        cell: list[Flowable] = [
            Paragraph(escape(exp.role), s["role"]),
            Paragraph(f'<b>{escape(exp.company)}</b>&nbsp;&nbsp;<font color="#{MUTED_HEX}">·&nbsp;&nbsp;<i>{escape(exp.period)}</i></font>', s["org"]),
            *(Paragraph(escape(bullet), s["bullet"], bulletText="•") for bullet in exp.bullets),
        ]
        if exp.technologies:
            chips = "&nbsp; ".join(
                f'<font backColor="#{CHIP_HEX}">&nbsp;{escape(tech).replace(" ", "&nbsp;")}&nbsp;</font>' for tech in exp.technologies
            )
            cell.append(Paragraph(chips, s["chips"]))
        return Table(
            [[cell]],
            colWidths=[MAIN_INNER],
            style=TableStyle([
                ("LINEBEFORE", (0, 0), (0, 0), 2, ACCENT),
                ("LEFTPADDING", (0, 0), (0, 0), 10),
                ("RIGHTPADDING", (0, 0), (0, 0), 0),
                ("TOPPADDING", (0, 0), (0, 0), 1),
                ("BOTTOMPADDING", (0, 0), (0, 0), 3),
            ]),
            spaceAfter=9,
        )

    def _callout(self, c: DocumentContent) -> Table:
        text = f'<b><font color="#{PRIMARY_HEX}">Demos técnicas, certificados y hoja de vida descargable</font></b><br/>{_link(c.portfolio, display_url(c.portfolio), ACCENT_HEX)}'
        return Table(
            [[Paragraph(text, self._s["callout"])]],
            colWidths=[MAIN_INNER],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), SURFACE),
                ("LINEBEFORE", (0, 0), (0, 0), 3, ACCENT),
                ("LEFTPADDING", (0, 0), (0, 0), 10),
                ("TOPPADDING", (0, 0), (0, 0), 7),
                ("BOTTOMPADDING", (0, 0), (0, 0), 7),
            ]),
        )
