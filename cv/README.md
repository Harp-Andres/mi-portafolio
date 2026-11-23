# cv/

- `qa/`: default web-facing variant (`input/` and `output/`).
- `devops-qa/`: isolated DevOps-oriented variant (`input/` and `output/`).
- Certificates stay global in `apps/web/public/certificados/` and are shared by both variants.

Apply requests with `pnpm cv:apply` (or the `cv-apply` MCP tool), check with `pnpm cv:status`. Full flow: `docs/CV_MANAGEMENT/WORKFLOW.md`.
