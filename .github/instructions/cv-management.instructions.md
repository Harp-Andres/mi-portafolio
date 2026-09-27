---
applyTo: "apps/web/src/utils/cv-data.ts,apps/web/src/components/CVDownloads.tsx,apps/web/src/utils/download-cv.ts,scripts/hv/**,apps/web/public/cv/**"
---

# CV / Hoja de Vida management skill

Role: `portfolio-cv-manager` (see `.github/agents/portfolio-cv-manager.agent.md`).

- Source of truth for CV content is `apps/web/src/utils/cv-data.ts` (or `packages/core/src/data/cv-data.ts` if shared). Never hardcode CV text elsewhere.
- Generated PDFs live in `apps/web/public/cv/`. Filenames must exactly match what `CVDownloads.tsx`/`download-cv.ts` reference — verify with `grep` before renaming.
- Any CV **or certificate** asset path must be built from `import.meta.env.BASE_URL` (see `apps/web/src/utils/public-asset.ts`), never a hardcoded root-absolute path like `/certificados/...` (this repo deploys under `/mi-portafolio/` on GitHub Pages — bare `/certificados/...` 404s).
- CV generation scripts live in `scripts/hv/`. Run via `pnpm generate:cv` (see `apps/web/package.json`).
- After regenerating a CV, verify the download E2E tests still pass (`apps/web/tests/e2e/02-cv-download.spec.ts`) using the real Playwright `download` event, not just a filesystem check.
