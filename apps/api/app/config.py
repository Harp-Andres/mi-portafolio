"""Filesystem layout of the CV flow inside the monorepo."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class CurriculumPaths:
    requests_dir: Path
    processed_dir: Path
    output_dir: Path
    web_public_dir: Path

    @classmethod
    def for_repo(cls, root: Path = REPO_ROOT) -> "CurriculumPaths":
        return cls(
            requests_dir=root / "cv" / "input" / "requests",
            processed_dir=root / "cv" / "input" / "processed",
            output_dir=root / "cv" / "output",
            web_public_dir=root / "apps" / "web" / "public",
        )

    @property
    def state_file(self) -> Path:
        """Structured twin of the Word/PDF documents; the web renders it."""
        return self.output_dir / "cv-data.json"

    @property
    def certificates_dir(self) -> Path:
        return self.web_public_dir / "certificados"
