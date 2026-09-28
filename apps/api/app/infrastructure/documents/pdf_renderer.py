"""Shared PDF rendering: metadata and fingerprint. Each layout (pdf_ats, pdf_visual) supplies its page and story."""

from __future__ import annotations

from abc import abstractmethod
from pathlib import Path
from typing import ClassVar

from reportlab.platypus import BaseDocTemplate, Flowable

from app.application.ports import DocumentRenderer, RenderedDocument
from app.domain.models import CurriculumVitae
from app.infrastructure.documents.content import FINGERPRINT_PREFIX, DocumentContent


class PdfCurriculumRenderer(DocumentRenderer):
    label: ClassVar[str]

    def __init__(self, output_path: Path, variant: str) -> None:
        self._output_path = output_path
        self._variant = variant

    @property
    def variant(self) -> str:
        return self._variant

    @property
    def output_path(self) -> Path:
        return self._output_path

    def render(self, cv: CurriculumVitae, fingerprint: str) -> RenderedDocument:
        content = DocumentContent.from_cv(cv)
        self._output_path.parent.mkdir(parents=True, exist_ok=True)
        metadata = {
            "title": f"{content.name} - CV {self.label}",
            "author": content.name,
            "subject": "Hoja de vida",
            "keywords": f"{FINGERPRINT_PREFIX}{fingerprint}",
        }
        self._document(self._output_path, content, metadata).build(self._story(content))
        return RenderedDocument(self._variant, self._output_path)

    @abstractmethod
    def _document(self, path: Path, content: DocumentContent, metadata: dict[str, str]) -> BaseDocTemplate: ...

    @abstractmethod
    def _story(self, content: DocumentContent) -> list[Flowable]: ...
