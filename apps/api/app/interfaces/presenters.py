"""Serializable views of use case results, shared by the CLI (--json) and the HTTP adapter."""

from __future__ import annotations

from pathlib import Path

from app.application.curriculum_status import StatusReport
from app.application.ports import RenderedDocument
from app.config import REPO_ROOT


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def status_payload(report: StatusReport) -> dict:
    return {
        "inSync": report.in_sync,
        "fingerprint": report.fingerprint,
        "jsonInSync": report.json_in_sync,
        "documents": [{"file": d.name, "exists": d.exists, "inSync": d.in_sync} for d in report.documents],
        "pendingRequests": [repo_relative(p) for p in report.pending_requests],
    }


def documents_payload(documents: list[RenderedDocument]) -> list[dict]:
    return [{"variant": d.variant, "format": d.format, "file": d.path.name} for d in documents]
