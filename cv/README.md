# cv/

- `input/requests/`: change requests (`.md`/`.txt`) saying what to add to or change in the Hoja de Vida. Start from `input/request-template.md`.
- `input/processed/`: requests already applied, archived by the backend with a timestamp.
- `output/`: the Word/PDF CV (ATS and Visual) rendered by the Python backend (`apps/api`), plus `cv-data.json`, the structured twin the web renders. All of them carry the same fingerprint.

Apply requests with `pnpm cv:apply` (or the `cv-apply` MCP tool), check with `pnpm cv:status`. Full flow: `docs/CV_MANAGEMENT/WORKFLOW.md`.
