---
applyTo: "cv/**,scripts/hv/**,packages/core/src/data/cv-data*,apps/web/src/utils/cv-data.ts,apps/web/src/components/CVDownloads.tsx,apps/web/src/utils/download-cv.ts,apps/web/public/certificados/**"
---

# CV / Hoja de Vida management skill

Role: `portfolio-cv-manager` (see `.github/agents/portfolio-cv-manager.agent.md`). User-facing flow: `docs/CV_MANAGEMENT/WORKFLOW.md`.

## Pipeline (one input, one direction)

`cv/input/cv-data.json` → `scripts/hv/generate-cv-pdf.py` → `cv/output/HV_2026_2_{ATS,Visual}_AndresRodriguez.{pdf,docx}` + `packages/core/src/data/cv-data.generated.json` → web (`@mportafolio/core` `CV_DATA`). `scripts/hv/sync-cv-downloads.mjs` copies `cv/output` to `apps/web/public/cv/` (gitignored) before `dev`/`build`.

- Edit CV content **only** in `cv/input/cv-data.json` (from chat, or `uv run scripts/hv/generate-cv-pdf.py other.json`, which validates and copies it over). Never edit the generated JSON, `cv/output/`, `apps/web/public/cv/` or add CV literals to TS/Python.
- Regenerate with MCP `cv-generate` or `pnpm generate:cv` (`uv run`, deps declared in the script header; add `--system-certs` behind corporate proxies). Check freshness with MCP `cv-status` or `pnpm sync:verify`.
- Each course appears once (`certificatesByCategory`, `learningPathsCertifications` or `officialCertifications`). The flat `certificates` list is derived by Python — don't add it to the input. `filePath` must exist under `apps/web/public` or be `null`; Python rejects the input otherwise and writes nothing.
- Certificate assets go in `apps/web/public/certificados/<Topic>/`. `apps/web/dist/` is build output; if a user points there, copy the file into `public/`.
- Web asset URLs must use `import.meta.env.BASE_URL` (`apps/web/src/utils/public-asset.ts`) because Pages serves under `/mi-portafolio/`. Download filenames in `CVDownloads.tsx`/`download-cv.ts` must match `OUTPUT_FILES` in the generator.
- Layout changes (not data) go in the generator's `build_ats_pdf` / `build_visual_pdf` / `build_docx`.

## Verification

- `pnpm -F @mportafolio/web test` (includes `cv-pipeline.test.ts`: generated JSON hash matches the input, every `filePath` exists, 4 output files present).
- Inspect generated docs by extracting text (`pypdf` with `strict=True`, `python-docx`), not by file size. `.gitattributes` keeps PDF/DOCX binary so `core.autocrlf` doesn't corrupt them.
- Download E2E: `apps/web/tests/e2e/02-cv-download.spec.ts` with the real Playwright `download` event.
