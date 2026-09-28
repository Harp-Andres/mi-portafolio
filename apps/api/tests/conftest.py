"""Every test runs against a throwaway copy of the repo layout, never the real cv/ folder."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from app.composition import CurriculumBackend, build_backend
from app.config import REPO_ROOT, CurriculumPaths
from app.infrastructure.persistence.json_codec import CurriculumJsonCodec

REAL_STATE = REPO_ROOT / "cv" / "output" / "cv-data.json"


@pytest.fixture
def paths(tmp_path: Path) -> CurriculumPaths:
    sandbox = CurriculumPaths.for_repo(tmp_path)
    sandbox.output_dir.mkdir(parents=True)
    shutil.copy(REAL_STATE, sandbox.state_file)
    data = json.loads(REAL_STATE.read_text(encoding="utf-8"))
    cv = CurriculumJsonCodec().decode(data)
    for file_path in cv.certificate_paths():
        placeholder = sandbox.web_public_dir / file_path.lstrip("/")
        placeholder.parent.mkdir(parents=True, exist_ok=True)
        placeholder.write_bytes(b"certificate")
    sandbox.requests_dir.mkdir(parents=True)
    return sandbox


@pytest.fixture
def backend(paths: CurriculumPaths) -> CurriculumBackend:
    return build_backend(paths)


@pytest.fixture
def write_request(paths: CurriculumPaths):
    def write(content: str, name: str = "request.md") -> Path:
        request = paths.requests_dir / name
        request.write_text(content, encoding="utf-8")
        return request

    return write
