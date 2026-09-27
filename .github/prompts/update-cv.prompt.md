---
description: "Update the Hoja de Vida from chat: edit cv/input/cv-data.json, regenerate with Python (PDF/DOCX + web data) and verify."
agent: portfolio-cv-manager
tools: [read, edit, execute, search, 'maestro/*']
argument-hint: "What changes (e.g. 'add course X — Udemy, 12h, DevOps & Cloud, certificate C:\\...\\cert.jpg')"
---

Update the CV with: ${input:change:What should change in the CV?}

1. Call `maestro-context`, then `cv-status`. Report if the generated data was already out of sync.
2. If a certificate file is provided, copy it to `apps/web/public/certificados/<Topic>/` with a descriptive kebab-case name.
3. Edit only `cv/input/cv-data.json` following `.github/instructions/cv-management.instructions.md` (each course once, `filePath` public path or `null`, integer `hours`).
4. Call `cv-generate` (fallback: `pnpm generate:cv`). Fix any validation error it lists and rerun.
5. Run `pnpm -F @mportafolio/web test`.
6. Reply in Spanish with: what changed, the regenerated files in `cv/output/`, test results, and ask whether to open a branch + PR.
