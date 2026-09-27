# OS Compatibility

Supported primary OS:
- Windows (PowerShell)
- Linux (bash)

Validation checklist:
- python, uv, node, pnpm available
- path and permission checks
- line ending and script execution policies

Troubleshooting focus:
- shell path resolution
- virtual environment activation
- executable lookup differences

Known issues (Windows):
- Renaming/moving the repo folder breaks pnpm links in `node_modules` (e.g. `Cannot find module …\node_modules\typescript\bin\tsc` or `…\vitest\vitest.mjs`). Reinstall from the repo root.
- `pnpm install` can fail with `ERR_PNPM_PACKAGE_MANAGER_REMOVE_MODULES_DIR … node_modules\pnpm … Acceso denegado (os error 5)` because pnpm runs from that folder. Use:
  `pnpm install --frozen-lockfile --config.manage-package-manager-versions=false`
- PowerShell treats backticks as escape characters: never pass Markdown with inline code as a CLI argument (e.g. `gh pr create --body`). Write it to a temp file and use `--body-file`.
- `npm run …` inside `apps/web` doesn't resolve workspace binaries reliably; use `pnpm run …` / `pnpm exec …`.
