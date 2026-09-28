"""Reads .md/.txt change requests written by the user or by the Copilot/Cursor agent.

    # Any title (ignored)
    ## Curso
    - titulo: Docker Mastery — Udemy
    - categoria: DevOps & Cloud
    - horas: 14
    - certificado: C:/Users/me/Downloads/docker.pdf

    ## Experiencia
    - empresa: ACME
    - cargo: QA Lead
    - periodo: 2026 – Actualidad
    - logros:
      - Built the automation framework
      - Cut regression time by 40%

Sections start with `##` (or `[Section]` in plain text). Text outside sections and HTML
comments are ignored, so templates can carry instructions.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Sequence

from app.application.ports import ChangeRequestParser
from app.domain.changes import CurriculumChange
from app.infrastructure.requests.sections import (
    DEFAULT_SECTIONS,
    RawSection,
    RequestFormatError,
    SectionBuilder,
    normalize,
)

_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_HEADING = re.compile(r"^(?:#{2,6}\s+(?P<md>.+?)\s*#*|\[(?P<txt>[^\]]+)\])$")
_KEY_VALUE = re.compile(r"^(?P<key>[^:]{1,40}?)\s*:\s*(?P<value>.*)$")
_BULLET = re.compile(r"^[-*+]\s+")


class TextChangeRequestParser(ChangeRequestParser):
    SUFFIXES = (".md", ".markdown", ".txt")

    def __init__(self, sections: Sequence[SectionBuilder] = DEFAULT_SECTIONS) -> None:
        self._builders = {normalize(name): builder for builder in sections for name in builder.names}

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in self.SUFFIXES

    def parse(self, request: Path) -> list[CurriculumChange]:
        text = _COMMENT.sub("", request.read_text(encoding="utf-8-sig"))
        return [self._build(section) for section in self._sections(text, request.parent)]

    def _build(self, section: RawSection) -> CurriculumChange:
        builder = self._builders.get(normalize(section.name))
        if builder is None:
            known = ", ".join(sorted({b.names[0] for b in self._builders.values()}))
            raise RequestFormatError(f"Unknown section {section.label}. Use one of: {known}")
        return builder.build(section)

    @staticmethod
    def _sections(text: str, base_dir: Path) -> list[RawSection]:
        sections: list[RawSection] = []
        current: RawSection | None = None
        last_key: str | None = None
        in_fence = False

        for number, raw in enumerate(text.splitlines(), start=1):
            stripped = raw.strip()
            if stripped.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence or not stripped:
                continue

            heading = _HEADING.match(stripped)
            if heading:
                current = RawSection(heading.group("md") or heading.group("txt"), number, base_dir)
                sections.append(current)
                last_key = None
                continue
            if current is None:
                continue

            indented = raw[: len(raw) - len(raw.lstrip())] != ""
            is_bullet = bool(_BULLET.match(stripped))
            content = _BULLET.sub("", stripped)
            pair = _KEY_VALUE.match(content)
            pending_list = last_key is not None and isinstance(current.fields.get(last_key), list)

            if pending_list and is_bullet and (indented or pair is None):
                current.fields[last_key].append(content)
            elif pair and not (indented and last_key):
                last_key = pair.group("key").strip()
                value = pair.group("value").strip()
                current.fields[last_key] = value if value else []
            elif last_key is not None:
                previous = current.fields[last_key]
                if isinstance(previous, list):
                    previous.append(content)
                else:
                    current.fields[last_key] = f"{previous} {content}".strip()
            else:
                raise RequestFormatError(f"Line {number}: expected 'field: value' inside {current.label}")
        return sections
