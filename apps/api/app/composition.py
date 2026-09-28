"""Composition root: the only module that knows which adapter implements each port."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.apply_change_request import ApplyChangeRequest
from app.application.curriculum_status import CurriculumStatus
from app.application.generate_documents import GenerateCurriculumDocuments
from app.application.ports import DocumentRenderer
from app.config import CurriculumPaths
from app.domain.validation import CurriculumValidator
from app.infrastructure.assets.certificate_store import PublicCertificateStore
from app.infrastructure.documents.docx_renderer import DocxCurriculumRenderer
from app.infrastructure.documents.fingerprint_readers import DocxFingerprintReader, PdfFingerprintReader
from app.infrastructure.documents.pdf_ats import AtsPdfRenderer
from app.infrastructure.documents.pdf_visual import VisualPdfRenderer
from app.infrastructure.persistence.json_repository import JsonCurriculumRepository
from app.infrastructure.requests.request_inbox import FolderRequestInbox
from app.infrastructure.requests.text_request_parser import TextChangeRequestParser

DOCUMENT_STEM = "HV_2026_2_{label}_AndresRodriguez"


@dataclass(frozen=True)
class CurriculumBackend:
    paths: CurriculumPaths
    apply_request: ApplyChangeRequest
    generate: GenerateCurriculumDocuments
    status: CurriculumStatus


def build_renderers(paths: CurriculumPaths, stem: str = DOCUMENT_STEM) -> list[DocumentRenderer]:
    out = paths.output_dir
    ats, visual = stem.format(label="ATS"), stem.format(label="Visual")
    return [
        AtsPdfRenderer(out / f"{ats}.pdf"),
        VisualPdfRenderer(out / f"{visual}.pdf"),
        DocxCurriculumRenderer(out / f"{ats}.docx", "ats", side_margin_pt=60),
        DocxCurriculumRenderer(out / f"{visual}.docx", "visual", side_margin_pt=54),
    ]


def build_backend(paths: CurriculumPaths | None = None) -> CurriculumBackend:
    paths = paths or CurriculumPaths.for_repo()
    repository = JsonCurriculumRepository(paths.state_file)
    validator = CurriculumValidator()
    renderers = build_renderers(paths)
    parser = TextChangeRequestParser()
    inbox = FolderRequestInbox(paths.requests_dir, paths.processed_dir, suffixes=parser.SUFFIXES)
    generate = GenerateCurriculumDocuments(repository, renderers, validator)
    return CurriculumBackend(
        paths=paths,
        apply_request=ApplyChangeRequest(
            repository,
            parsers=[parser],
            certificates=PublicCertificateStore(paths.web_public_dir, paths.certificates_dir),
            validator=validator,
            generator=generate,
            inbox=inbox,
        ),
        generate=generate,
        status=CurriculumStatus(repository, renderers, [PdfFingerprintReader(), DocxFingerprintReader()], inbox),
    )
