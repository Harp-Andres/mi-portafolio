"""Use case: render the Word/PDF CV and publish the matching JSON for the web."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from app.application.ports import CurriculumRepository, DocumentRenderer, RenderedDocument
from app.domain.models import CurriculumVitae
from app.domain.validation import CurriculumValidator


@dataclass(frozen=True)
class GenerationResult:
    fingerprint: str
    documents: list[RenderedDocument]


class GenerateCurriculumDocuments:
    def __init__(
        self,
        repository: CurriculumRepository,
        renderers: Sequence[DocumentRenderer],
        validator: CurriculumValidator,
    ) -> None:
        self._repository = repository
        self._renderers = renderers
        self._validator = validator

    def execute(self, cv: CurriculumVitae | None = None) -> GenerationResult:
        cv = cv if cv is not None else self._repository.load()
        self._validator.ensure_valid(cv)
        fingerprint = cv.fingerprint()
        documents = [renderer.render(cv, fingerprint) for renderer in self._renderers]
        # The JSON is written last so the web never points at documents that failed to render.
        self._repository.save(cv, documents)
        return GenerationResult(fingerprint, documents)
