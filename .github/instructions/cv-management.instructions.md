---
applyTo: "cv/**,apps/api/**,scripts/hv/**,packages/core/src/data/cv-data*,apps/web/src/utils/cv-data.ts,apps/web/src/components/CVDownloads.tsx,apps/web/src/utils/download-cv.ts,apps/web/public/certificados/**"
---

# CV / Hoja de Vida management skill

Role: `portfolio-cv-manager` (see `.github/agents/portfolio-cv-manager.agent.md`). User-facing flow: `docs/CV_MANAGEMENT/WORKFLOW.md`.

## Pipeline (three responsibilities, one direction)

1. **Input**: a change request `.md`/`.txt` (`cv/input/requests/`, any user path, or chat instructions written in the `cv/input/request-template.md` format).
2. **Backend** `apps/api` (`python -m app status|apply|generate`, pnpm `cv:status|cv:apply|cv:generate`, MCP `cv-status|cv-apply|cv-generate`): parses the request into domain commands, applies them to the `CurriculumVitae` aggregate, validates, imports certificates into `apps/web/public/certificados/<Provider>/`, renders `cv/output/HV_2026_2_{ATS,Visual}_AndresRodriguez.{pdf,docx}` and writes `cv/output/cv-data.json`, then archives the request in `cv/input/processed/`. A rejected request changes nothing.
3. **Web**: `@mportafolio/core` imports `cv/output/cv-data.json` (`CV_DATA`, `CV_DOCUMENTS`, `getCertificateLinks`); `scripts/hv/sync-cv-downloads.mjs` copies `cv/output` to `apps/web/public/cv/` (gitignored) before `dev`/`build`. Download names come from `_meta.documents`, not literals.

## Rules

- Never edit `cv/output/` by hand or add CV literals to TS/Python; change the CV only through a request.
- Word, PDF and JSON share `_meta.fingerprint` (PDF `Keywords`, DOCX `identifier`). If they diverge, run `pnpm cv:generate`.
- Backend layers: `domain` (no I/O) → `application` (use cases on ports) → `infrastructure` (parser, JSON repo, renderers, certificate store) → `interfaces` (CLI, HTTP) wired only in `composition.py`. New request types = a `CurriculumChange` subclass + a `SectionBuilder`; layout changes go in `infrastructure/documents/`.
- Web asset URLs must use `import.meta.env.BASE_URL` (`apps/web/src/utils/public-asset.ts`) because Pages serves under `/mi-portafolio/`. `apps/web/dist/` is build output.
- `uv run` behind a corporate proxy needs `--system-certs`.

## Verification

- `pnpm test:backend` (domain, parser, use cases end-to-end on a sandbox repo, CLI, HTTP).
- `pnpm -F @mportafolio/web test` (includes `cv-pipeline.test.ts`: listed documents exist, PDFs carry the JSON fingerprint, every certificate `filePath` exists).
- Inspect generated docs by extracting text (`pypdf` with `strict=True`, `python-docx`), not by file size. `.gitattributes` keeps PDF/DOCX binary so `core.autocrlf` doesn't corrupt them.
- Download E2E: `apps/web/tests/e2e/02-cv-download.spec.ts` with the real Playwright `download` event.
