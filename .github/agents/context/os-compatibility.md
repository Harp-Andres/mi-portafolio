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
- Python scripts that print emoji crash on the cp1252 console (`UnicodeEncodeError: 'charmap' codec`). Set `$env:PYTHONIOENCODING='utf-8'` first.
- `uv` behind a TLS-intercepting proxy fails with `invalid peer certificate: UnknownIssuer`; add `--system-certs`.
- Stopping a `pnpm exec vite` shell with `Stop-Process` can leave the child `node.exe` listening. Find it with `Get-NetTCPConnection -LocalPort <port> -State Listen` and stop that PID.
- After renaming the repo folder, console scripts in `agent/.venv` (e.g. `pytest.exe`) fail with `uv trampoline failed to canonicalize script path`. Use `uv run python -m pytest …`, or recreate the venv (`Remove-Item -Recurse agent\.venv; uv sync`).
- The CV backend CLI (`python -m app`) reconfigures stdout to UTF-8 itself, so `pnpm cv:*` doesn't need `PYTHONIOENCODING`.
- A half-deleted venv can leave `*.dist-info` folders without `RECORD`: `uv` then reports packages as installed while imports fail, and pytest loads dead plugins. Run `uv sync --reinstall` and, for pytest, `$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'`.
- `core.autocrlf=true` corrupts uncompressed PDFs that git detects as text. The root `.gitattributes` marks binaries; to repair an existing checkout, delete the file and run `git checkout -- <file>`.
