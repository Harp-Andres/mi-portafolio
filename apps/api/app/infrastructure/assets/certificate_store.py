"""Certificates live in apps/web/public/certificados/<folder>/ and are linked as /certificados/..."""

from __future__ import annotations

import filecmp
import re
import shutil
from pathlib import Path

from app.application.ports import CertificateStore
from app.domain.changes import CertificateAttachment
from app.domain.errors import CurriculumError

_UNSAFE = re.compile(r"[^\w.\- ]+", re.UNICODE)


def _safe(part: str) -> str:
    return _UNSAFE.sub("-", part).strip(" .-") or "General"


class PublicCertificateStore(CertificateStore):
    ALLOWED_SUFFIXES = (".pdf", ".jpg", ".jpeg", ".png", ".webp")

    def __init__(self, public_dir: Path, certificates_dir: Path) -> None:
        self._public_dir = public_dir
        self._certificates_dir = certificates_dir
        self._created: set[Path] = set()

    def import_file(self, attachment: CertificateAttachment) -> str:
        source = Path(attachment.source)
        if not source.is_file():
            raise CurriculumError(f"Certificate file not found: {source}")
        if source.suffix.lower() not in self.ALLOWED_SUFFIXES:
            raise CurriculumError(f"Certificate must be one of {', '.join(self.ALLOWED_SUFFIXES)}: {source.name}")

        folder = self._certificates_dir.joinpath(*(_safe(p) for p in re.split(r"[\\/]+", attachment.folder) if p))
        target = self._free_target(folder / _safe(source.name), source)
        if not target.exists():
            folder.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            self._created.add(target)
        return "/" + target.relative_to(self._public_dir).as_posix()

    def exists(self, file_path: str) -> bool:
        return self._resolve(file_path).is_file()

    def discard(self, file_path: str) -> None:
        target = self._resolve(file_path)
        if target in self._created:
            target.unlink(missing_ok=True)
            self._created.discard(target)

    def _resolve(self, file_path: str) -> Path:
        return self._public_dir / file_path.lstrip("/")

    @staticmethod
    def _free_target(target: Path, source: Path) -> Path:
        """Reuses an identical file; never overwrites a different one."""
        candidate, counter = target, 1
        while candidate.exists() and not filecmp.cmp(candidate, source, shallow=False):
            candidate = target.with_name(f"{target.stem}-{counter}{target.suffix}")
            counter += 1
        return candidate
