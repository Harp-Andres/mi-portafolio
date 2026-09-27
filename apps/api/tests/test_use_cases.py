"""End-to-end through the real adapters: request -> Word/PDF + JSON, on a sandbox repo."""

from __future__ import annotations

import json

import pytest
from docx import Document

from app.domain.errors import CurriculumError, DuplicateEntryError

COURSE_REQUEST = """## Curso
- titulo: k6 Performance Testing — Udemy
- categoria: Calidad & QA
- horas: 9
- certificado: ../k6.pdf
"""


def docx_text(path) -> str:
    return "\n".join(p.text for p in Document(str(path)).paragraphs)


def test_generate_renders_every_document_stamped_with_the_json_fingerprint(backend, paths):
    result = backend.generate.execute()

    assert sorted(d.path.name for d in result.documents) == sorted(r.name for r in paths.output_dir.glob("HV_*"))
    report = backend.status.execute()
    assert report.in_sync and report.fingerprint == result.fingerprint
    meta = json.loads(paths.state_file.read_text(encoding="utf-8"))["_meta"]
    assert meta["fingerprint"] == result.fingerprint
    assert {(d["variant"], d["format"]) for d in meta["documents"]} == {
        ("ats", "pdf"), ("visual", "pdf"), ("ats", "docx"), ("visual", "docx"),
    }


def test_apply_request_updates_documents_json_certificates_and_archives_it(backend, paths, write_request):
    (paths.requests_dir.parent / "k6.pdf").write_bytes(b"%PDF k6")
    request = write_request(COURSE_REQUEST)

    result = backend.apply_request.execute(request)

    assert result.applied == ["Course added to 'Calidad & QA': k6 Performance Testing — Udemy"]
    data = json.loads(paths.state_file.read_text(encoding="utf-8"))
    course = data["certificatesByCategory"]["Calidad & QA"][-1]
    assert course == {"title": "k6 Performance Testing — Udemy", "filePath": "/certificados/Udemy/k6.pdf", "hours": 9}
    assert (paths.certificates_dir / "Udemy" / "k6.pdf").read_bytes() == b"%PDF k6"
    ats_docx = next(d.path for d in result.generation.documents if d.variant == "ats" and d.format == "docx")
    assert "k6 Performance Testing — Udemy (9h)" in docx_text(ats_docx)
    assert not request.exists() and result.archived_request.parent == paths.processed_dir
    assert backend.status.execute().in_sync


def test_rejected_request_changes_nothing(backend, paths, write_request):
    backend.generate.execute()
    before = paths.state_file.read_text(encoding="utf-8")
    existing = json.loads(before)["officialCertifications"][0]["title"]
    (paths.requests_dir.parent / "k6.pdf").write_bytes(b"%PDF k6")
    request = write_request(COURSE_REQUEST + f"\n## Curso\n- titulo: {existing}\n- categoria: QA\n")

    with pytest.raises(DuplicateEntryError):
        backend.apply_request.execute(request)

    assert paths.state_file.read_text(encoding="utf-8") == before
    assert not (paths.certificates_dir / "Udemy" / "k6.pdf").exists()
    assert request.exists() and not paths.processed_dir.exists()


def test_missing_certificate_file_is_reported(backend, write_request):
    request = write_request(COURSE_REQUEST.replace("../k6.pdf", "nope.pdf"))
    with pytest.raises(CurriculumError, match="Certificate file not found"):
        backend.apply_request.execute(request)


def test_status_lists_pending_requests_and_stale_documents(backend, write_request):
    request = write_request("## Idioma\n- idioma: Francés\n- nivel: A1\n", name="idioma.txt")
    report = backend.status.execute()
    assert report.pending_requests == [request]
    assert not report.in_sync
