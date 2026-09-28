"""Read back the fingerprint stamped by the renderers (PDF keywords / DOCX identifier)."""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document

from app.application.ports import FingerprintReader
from app.infrastructure.documents.content import FINGERPRINT_PREFIX

_PDF_STAMP = re.compile(re.escape(FINGERPRINT_PREFIX).encode() + rb"([0-9a-f]{64})")


class PdfFingerprintReader(FingerprintReader):
    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".pdf"

    def read(self, path: Path) -> str | None:
        match = _PDF_STAMP.search(path.read_bytes())
        return match.group(1).decode() if match else None


class DocxFingerprintReader(FingerprintReader):
    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".docx"

    def read(self, path: Path) -> str | None:
        return Document(str(path)).core_properties.identifier or None
