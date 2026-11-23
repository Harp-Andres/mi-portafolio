"""Filesystem layout of the CV flow inside the monorepo."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CV_VARIANT = "qa"
SUPPORTED_CV_VARIANTS = (DEFAULT_CV_VARIANT, "devops-qa")


@dataclass(frozen=True)
class CurriculumPaths:
    variant: str
    requests_dir: Path
    processed_dir: Path
    output_dir: Path
    web_public_dir: Path

    @classmethod
    def for_repo(cls, root: Path = REPO_ROOT, variant: str = DEFAULT_CV_VARIANT) -> "CurriculumPaths":
        if variant not in SUPPORTED_CV_VARIANTS:
            supported = ", ".join(SUPPORTED_CV_VARIANTS)
            raise ValueError(f"Unsupported CV variant '{variant}'. Expected one of: {supported}")
        variant_dir = root / "cv" / variant
        return cls(
            variant=variant,
            requests_dir=variant_dir / "input" / "requests",
            processed_dir=variant_dir / "input" / "processed",
            output_dir=variant_dir / "output",
            web_public_dir=root / "apps" / "web" / "public",
        )

    @property
    def state_file(self) -> Path:
        """Structured twin of the Word/PDF documents; the web renders it."""
        return self.output_dir / "cv-data.json"

    @property
    def certificates_dir(self) -> Path:
        return self.web_public_dir / "certificados"
