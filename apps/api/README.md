# apps/api — CV backend

Python backend that owns the Hoja de Vida processing. It takes a change request (`.md`/`.txt`),
applies it to the CV, validates it, and renders the Word and PDF CV (ATS and Visual) plus
`cv/output/cv-data.json`, the structured twin the web renders. User flow:
[`docs/CV_MANAGEMENT/WORKFLOW.md`](../../docs/CV_MANAGEMENT/WORKFLOW.md).

## Commands (from the repo root)

| Command | What it does |
|---------|--------------|
| `pnpm cv:status` | Are Word/PDF/JSON rendered from the same CV? Which requests are pending? (`--json` for machines) |
| `pnpm cv:apply [-- path.md]` | Apply pending requests in `cv/input/requests/` (or the given files) and regenerate everything |
| `pnpm cv:generate` | Re-render Word/PDF/JSON from the current CV (after a layout change) |
| `pnpm test:backend` | pytest suite (runs on a sandbox copy, never touches `cv/`) |
| `pnpm dev:backend` | Optional local HTTP API over the same use cases (`/api/cv/status`, `/api/cv/requests`, ...) |

All of them run `uv run --project apps/api python -m app …`. Behind a TLS-intercepting proxy add `--system-certs`.

## Architecture (`app/`)

```text
interfaces/  cli.py, http.py, presenters.py      → adapters for people, pnpm, MCP and HTTP
composition.py                                     → the only place wiring ports to adapters
application/ ports.py + one module per use case    → ApplyChangeRequest, GenerateCurriculumDocuments, CurriculumStatus
domain/      models.py, changes.py, validation.py  → CurriculumVitae aggregate, change commands, rules (no I/O)
infrastructure/
  requests/     text_request_parser.py, sections.py, request_inbox.py
  persistence/  json_codec.py, json_repository.py
  documents/    content.py, pdf_renderer.py, docx_renderer.py, fingerprint_readers.py, theme.py
  assets/       certificate_store.py
```

- **Single responsibility**: parsing, applying, validating, rendering, persisting and archiving are separate classes.
- **Open/closed**: a new request type is a `CurriculumChange` subclass plus a `SectionBuilder`; a new document format is a `DocumentRenderer`.
- **Dependency inversion**: use cases depend on `application/ports.py`; adapters are injected in `composition.py`.
- Word, PDF and JSON carry the same content fingerprint so the web can prove it shows what the documents say.
