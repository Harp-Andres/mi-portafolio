"""CV state stored as cv/output/cv-data.json, next to the Word/PDF it was rendered into."""

from __future__ import annotations

import json
from pathlib import Path

from app.application.ports import CurriculumRepository, RenderedDocument
from app.domain.errors import CurriculumError
from app.domain.models import CurriculumVitae
from app.infrastructure.persistence.json_codec import CurriculumJsonCodec


class JsonCurriculumRepository(CurriculumRepository):
    META_KEY = "_meta"

    def __init__(self, path: Path, codec: CurriculumJsonCodec | None = None) -> None:
        self._path = path
        self._codec = codec or CurriculumJsonCodec()

    def load(self) -> CurriculumVitae:
        try:
            return self._codec.decode(self._read())
        except KeyError as missing:
            raise CurriculumError(f"{self._path.name} is missing the field {missing}") from None

    def save(self, cv: CurriculumVitae, documents: list[RenderedDocument]) -> None:
        data = self._codec.encode(cv)
        data[self.META_KEY] = {
            "fingerprint": cv.fingerprint(),
            "documents": [{"variant": d.variant, "format": d.format, "file": d.path.name} for d in documents],
            "generatedBy": "apps/api (python -m app)",
            "note": "Generated with the Word/PDF in this folder. Change the CV with a request in cv/input/requests.",
        }
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def stored_fingerprint(self) -> str | None:
        return self._read().get(self.META_KEY, {}).get("fingerprint")

    def _read(self) -> dict:
        if not self._path.is_file():
            raise CurriculumError(f"CV state not found: {self._path}")
        return json.loads(self._path.read_text(encoding="utf-8"))
