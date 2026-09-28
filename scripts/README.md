# scripts/

Reusable repo scripts. Day-to-day work goes through the `pnpm` scripts in the root `package.json`
and the `gh` CLI; add a script here only when it is reused and a one-line `pnpm`/`gh` command is not enough.

| Script | Run by | What it does |
| --- | --- | --- |
| `hv/sync-cv-downloads.mjs` | `pnpm dev`, `pnpm build`, `pnpm sync:cv` | Copies the Word/PDF from `cv/output/` to `apps/web/public/cv/` (gitignored) so the web serves the same CV the backend rendered |

## Common commands

| Task | Command |
| --- | --- |
| Type-check, unit tests, build | `pnpm lint` · `pnpm test` · `pnpm build` |
| E2E tests | `pnpm test:e2e` |
| CV backend and maestro agent tests | `pnpm test:backend` · `pnpm test:agent` |
| Everything CI runs, before a PR | `pnpm release` |
| CV status / apply a change request | `pnpm cv:status` · `pnpm cv:apply` |
| Open a PR (Windows: always use a body file) | `gh pr create --base main --title "..." --body-file body.md` |
| Watch the PR checks | `gh pr checks <number> --watch` |
