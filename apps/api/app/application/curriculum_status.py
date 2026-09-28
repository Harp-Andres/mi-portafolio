"""Use case: report whether the Word/PDF documents and the web JSON match the current CV."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from app.application.ports import (
    CurriculumRepository,
    DocumentRenderer,
    FingerprintReader,
    RequestInbox,
)


@dataclass(frozen=True)
class DocumentState:
    name: str
    exists: bool
    in_sync: bool


@dataclass(frozen=True)
class StatusReport:
    fingerprint: str
    json_in_sync: bool
    documents: list[DocumentState]
    pending_requests: list[Path]

    @property
    def in_sync(self) -> bool:
        return self.json_in_sync and all(doc.in_sync for doc in self.documents)


class CurriculumStatus:
    def __init__(
        self,
        repository: CurriculumRepository,
        renderers: Sequence[DocumentRenderer],
        readers: Sequence[FingerprintReader],
        inbox: RequestInbox,
    ) -> None:
        self._repository = repository
        self._renderers = renderers
        self._readers = readers
        self._inbox = inbox

    def execute(self) -> StatusReport:
        fingerprint = self._repository.load().fingerprint()
        return StatusReport(
            fingerprint=fingerprint,
            json_in_sync=self._repository.stored_fingerprint() == fingerprint,
            documents=[self._document_state(r.output_path, fingerprint) for r in self._renderers],
            pending_requests=self._inbox.pending(),
        )

    def _document_state(self, path: Path, fingerprint: str) -> DocumentState:
        if not path.is_file():
            return DocumentState(path.name, exists=False, in_sync=False)
        reader = next((r for r in self._readers if r.supports(path)), None)
        stamped = reader.read(path) if reader else None
        return DocumentState(path.name, exists=True, in_sync=stamped == fingerprint)
