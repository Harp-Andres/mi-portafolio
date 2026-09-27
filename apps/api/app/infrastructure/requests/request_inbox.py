"""cv/input/requests holds pending requests; applied ones are archived in cv/input/processed."""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Callable, Sequence

from app.application.ports import RequestInbox


class FolderRequestInbox(RequestInbox):
    def __init__(
        self,
        requests_dir: Path,
        processed_dir: Path,
        suffixes: Sequence[str] = (".md", ".markdown", ".txt"),
        clock: Callable[[], datetime] = datetime.now,
    ) -> None:
        self._requests_dir = requests_dir
        self._processed_dir = processed_dir
        self._suffixes = suffixes
        self._clock = clock

    def pending(self) -> list[Path]:
        if not self._requests_dir.is_dir():
            return []
        return sorted(
            path
            for path in self._requests_dir.iterdir()
            if path.is_file() and path.suffix.lower() in self._suffixes and not path.name.startswith(".")
        )

    def archive(self, request: Path) -> Path:
        self._processed_dir.mkdir(parents=True, exist_ok=True)
        target = self._processed_dir / f"{self._clock():%Y%m%d-%H%M%S}-{request.name}"
        if request.resolve().parent == self._requests_dir.resolve():
            shutil.move(str(request), target)
        else:
            shutil.copy2(request, target)
        return target
