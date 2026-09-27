"""Ports the use cases depend on. Infrastructure provides the implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from app.domain.changes import CertificateAttachment, CurriculumChange
from app.domain.models import CurriculumVitae


@dataclass(frozen=True)
class RenderedDocument:
    variant: str
    path: Path

    @property
    def format(self) -> str:
        return self.path.suffix.lstrip(".").lower()


class CurriculumRepository(ABC):
    """Persists the current CV. Its file is also the data the web renders."""

    @abstractmethod
    def load(self) -> CurriculumVitae: ...

    @abstractmethod
    def save(self, cv: CurriculumVitae, documents: list[RenderedDocument]) -> None: ...

    @abstractmethod
    def stored_fingerprint(self) -> str | None: ...


class ChangeRequestParser(ABC):
    """Turns a user request (.md, .txt, ...) into change commands."""

    @abstractmethod
    def supports(self, path: Path) -> bool: ...

    @abstractmethod
    def parse(self, request: Path) -> list[CurriculumChange]: ...


class CertificateStore(ABC):
    @abstractmethod
    def import_file(self, attachment: CertificateAttachment) -> str:
        """Copies the certificate where the web serves it and returns its public path."""

    @abstractmethod
    def exists(self, file_path: str) -> bool: ...

    @abstractmethod
    def discard(self, file_path: str) -> None:
        """Undoes an import when the request is rejected."""


class DocumentRenderer(ABC):
    """Renders one CV document (e.g. ATS PDF) stamped with the CV fingerprint."""

    @property
    @abstractmethod
    def variant(self) -> str: ...

    @property
    @abstractmethod
    def output_path(self) -> Path: ...

    @abstractmethod
    def render(self, cv: CurriculumVitae, fingerprint: str) -> RenderedDocument: ...


class FingerprintReader(ABC):
    """Reads the fingerprint stamped in an already rendered document."""

    @abstractmethod
    def supports(self, path: Path) -> bool: ...

    @abstractmethod
    def read(self, path: Path) -> str | None: ...


class RequestInbox(ABC):
    """Where pending requests wait and where applied ones are archived."""

    @abstractmethod
    def pending(self) -> list[Path]: ...

    @abstractmethod
    def archive(self, request: Path) -> Path: ...
