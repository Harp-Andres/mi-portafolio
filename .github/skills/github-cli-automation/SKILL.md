---
name: github-cli-automation
description: pnpm and gh CLI commands to test, build, open and track pull requests and GitHub Actions runs in mi-portafolio, with the PowerShell gotchas. Use when the user asks to run checks, validate/build, create/merge pull requests or inspect CI via the gh CLI.
---

# GitHub CLI Automation Skill

Everything goes through the root `package.json` scripts and the `gh` CLI; there are no wrapper scripts.
Through the maestro MCP the same checks are `skill-quality-gate-runner`, `skill-release-orchestrator` and
`skill-git-workflow-manager`.

## Checks (repo root)

| Goal | Command |
| --- | --- |
| Type-check | `pnpm lint` (all packages: `pnpm lint:all`) |
| Web unit tests (single run) | `pnpm test` |
| E2E | `pnpm test:e2e` |
| CV backend / maestro agent | `pnpm test:backend` / `pnpm test:agent` |
| Everything CI runs | `pnpm release` |
| Production build | `pnpm build` |

## Branch → PR → merge

```powershell
git checkout main; git pull --ff-only origin main
git checkout -b feat/my-change
# ... edit, then stage explicit paths
git add apps/web/src/components/Footer.tsx
git commit -m "feat(web): short subject" -m "Why it changed."
git push -u origin feat/my-change
gh pr create --base main --title "feat(web): short subject" --body-file "$env:TEMP\pr-body.md"
gh pr checks <number> --watch --interval 20
```

The user merges; never push to `main`.

## CI

| Goal | Command |
| --- | --- |
| Latest runs of a branch | `gh run list --branch <branch> --limit 5` |
| Jobs and steps of a run | `gh run view <id>` |
| Only the failing log lines | `gh run view <id> --log-failed` |
| Re-run failed jobs | `gh run rerun <id> --failed` |

Pipeline (`.github/workflows/deploy.yml`): install → lint, test-unit, test-backend, test-agent, test-e2e in
parallel → build → deploy (push to `main` only) → notify.

## PowerShell gotchas

- **PR bodies with Markdown:** backticks are PowerShell escape characters, so an inline `--body "…`code`…"` gets
  mangled (e.g. `unknown flag: --noEmit`). Write the body to a temp file, pass `--body-file`, then delete it.
- **Commit messages:** repeated `-m` flags for subject and paragraphs instead of a multi-line string.
- **Staging:** add files explicitly; never `git add -A` (tracked `.pyc` files and local logs may be modified).
- **`--jq` filters:** PowerShell mangles `\(...)` interpolation and splits filters that contain inner double
  quotes (`accepts at most 1 arg(s)`). Use the default table output or pipe `--json` into `ConvertFrom-Json`.
- **pnpm 12:** there is no `-s`/`--silent` flag (`unexpected argument '-s'`); use `pnpm run <script>`.
  Its stderr shows up as `NativeCommandError`; judge by the exit code.
- **After opening a PR:** `gh pr checks` may say "no checks reported" for a few seconds; wait and retry.

## Requirements

- GitHub CLI authenticated (`winget install --id GitHub.cli`, then `gh auth login`)
- pnpm 12+, Node 20+ (CI uses 24), uv for the Python checks

**Repository:** https://github.com/Harp-Andres/mi-portafolio (renamed from `MiPortafolio`; always use the new URL).
