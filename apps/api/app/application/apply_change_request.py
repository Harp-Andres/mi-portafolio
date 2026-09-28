"""Use case: apply a user change request (.md/.txt) to the CV and regenerate the documents."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from app.application.generate_documents import GenerateCurriculumDocuments, GenerationResult
from app.application.ports import (
    CertificateStore,
    ChangeRequestParser,
    CurriculumRepository,
    RequestInbox,
)
from app.domain.changes import CurriculumChange
from app.domain.errors import CurriculumError, InvalidCurriculumError
from app.domain.validation import CurriculumValidator


class UnsupportedRequestError(CurriculumError):
    pass


@dataclass(frozen=True)
class ApplyResult:
    applied: list[str]
    generation: GenerationResult
    archived_request: Path


class ApplyChangeRequest:
    def __init__(
        self,
        repository: CurriculumRepository,
        parsers: Sequence[ChangeRequestParser],
        certificates: CertificateStore,
        validator: CurriculumValidator,
        generator: GenerateCurriculumDocuments,
        inbox: RequestInbox,
    ) -> None:
        self._repository = repository
        self._parsers = parsers
        self._certificates = certificates
        self._validator = validator
        self._generator = generator
        self._inbox = inbox

    def execute(self, request: Path) -> ApplyResult:
        changes = self._parse(request)
        cv = self._repository.load()
        imported: list[str] = []
        try:
            for change in changes:
                self._import_certificate(change, imported)
                change.apply(cv)
            self._validator.ensure_valid(cv)
            self._ensure_certificates_exist(cv.certificate_paths())
            generation = self._generator.execute(cv)
        except Exception:
            for file_path in imported:
                self._certificates.discard(file_path)
            raise
        return ApplyResult(
            applied=[change.describe() for change in changes],
            generation=generation,
            archived_request=self._inbox.archive(request),
        )

    def _parse(self, request: Path) -> list[CurriculumChange]:
        if not request.is_file():
            raise UnsupportedRequestError(f"Request not found: {request}")
        parser = next((p for p in self._parsers if p.supports(request)), None)
        if parser is None:
            raise UnsupportedRequestError(f"Unsupported request type '{request.suffix}' (use .md or .txt)")
        changes = parser.parse(request)
        if not changes:
            raise UnsupportedRequestError(f"{request.name} does not contain any change")
        return changes

    def _import_certificate(self, change: CurriculumChange, imported: list[str]) -> None:
        attachment = change.attachment()
        if attachment is None:
            return
        file_path = self._certificates.import_file(attachment)
        imported.append(file_path)
        change.attach(file_path)

    def _ensure_certificates_exist(self, file_paths) -> None:
        missing = [path for path in file_paths if not self._certificates.exists(path)]
        if missing:
            raise InvalidCurriculumError([f"certificate file not found: {path}" for path in missing])
