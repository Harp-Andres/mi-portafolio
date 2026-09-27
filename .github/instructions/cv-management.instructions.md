---
applyTo: "apps/web/src/utils/cv-data.ts,apps/web/src/components/CVDownloads.tsx,apps/web/src/utils/download-cv.ts,scripts/hv/**,apps/web/public/cv/**"
---

# CV / Hoja de Vida management skill

Role: `portfolio-cv-manager` (see `.github/agents/portfolio-cv-manager.agent.md`).

- Source of truth for CV content is `apps/web/src/utils/cv-data.ts` (or `packages/core/src/data/cv-data.ts` if shared). Never hardcode CV text elsewhere.
- Generated PDFs live in `apps/web/public/cv/`. Filenames must exactly match what `CVDownloads.tsx`/`download-cv.ts` reference — verify with `grep` before renaming.
- Any CV **or certificate** asset path must be built from `import.meta.env.BASE_URL` (see `apps/web/src/utils/public-asset.ts`), never a hardcoded root-absolute path like `/certificados/...` (this repo deploys under `/mi-portafolio/` on GitHub Pages — bare `/certificados/...` 404s).
- CV generation scripts live in `scripts/hv/`. Run via `pnpm generate:cv` (see `apps/web/package.json`). On Windows without the Python deps installed, use:
  `$env:PYTHONIOENCODING='utf-8'; uv run --system-certs --no-project --with python-docx --with reportlab python scripts/hv/generate-cv-pdf.py`
  It writes the 4 files (ATS/Visual × PDF/DOCX) to both `apps/web/public/cv/` and `Hoja De Vida/`.
- CV content is duplicated in three places that must stay in sync: `apps/web/src/utils/cv-data.ts`, `packages/core/src/data/cv-data.ts` (both `certificates` and `certificatesByCategory`), and the `DATA` dict in `scripts/hv/generate-cv-pdf.py`. For a new course, update all three, add the asset, then regenerate.
- Certificate assets go in `apps/web/public/certificados/<Topic>/`. `apps/web/dist/` is gitignored build output that gets wiped on every build, so a file that only exists there never reaches GitHub Pages. If a user points at `dist/`, copy the file into `public/`.
- Verify generated docs by extracting text (`pypdf` with `strict=True`, `python-docx`), not by file size. `.gitattributes` marks PDF/DOCX/images as `binary`; without it `core.autocrlf` corrupts uncompressed PDFs on checkout.
- After regenerating a CV, verify the download E2E tests still pass (`apps/web/tests/e2e/02-cv-download.spec.ts`) using the real Playwright `download` event, not just a filesystem check.
