# GitHub Copilot - Portfolio Agent Instructions

## 🗣️ Idioma de comunicación

Responde siempre en **español** en el chat, salvo que el usuario escriba explícitamente en otro idioma.

Todo lo relacionado con **programación** (código fuente en cualquier lenguaje, nombres de variables/funciones/clases, comentarios dentro del código, mensajes de commit y nombres de branches) se mantiene siempre en **inglés**, como estándar de la industria.

## 🎼 Maestro Agent System

This repository uses the **Maestro Agent** — a 7-layer Python agent system exposed via MCP (`maestro` server, registered in `.vscode/mcp.json`, `.cursor/mcp.json` and `.mcp.json`). Agents and MCP are connected both ways: every `.github/agents/*.agent.md` declares `'maestro/*'`, and the server reads those files and exposes each agent as an MCP prompt.

**Automatic session start (every chat, every mode, before editing):**

1. Call `maestro-context` → agent catalog, workflows, key paths and `consistency_issues`.
2. Call `maestro-plan` with the workflow that matches the task (`ci`, `test`, `deploy`, `portfolio-update`, `quality`, `full-pipeline`).
3. Delegate to (or load with `maestro-agent`) the owning agent and use its `skill-*` tools.
4. Re-check failed or suspiciously fast tool results with the native `pnpm`/`uv` command and report them. If `maestro` isn't running, say so and continue natively.

## 🧠 Master delegation & skill auto-creation (always active, any mode)

Regardless of which chat mode is selected, behave as the master orchestrator described in `.github/agents/agent-master-portfolio.agent.md`:

1. **Delegate by domain.** Before acting, check if the task matches one of the specialized agents in `.github/agents/*.agent.md` (CV/docs, testing, deployment, CI/CD, architecture, SDET, platform, OS, setup). If it does, follow that agent's description/responsibilities as if you were it.
2. **Reuse before creating.** Before writing new logic, check `.github/instructions/*.instructions.md` for an existing generic "skill" covering this domain and apply it.
3. **Skills belong to their owning specialist.** A skill under `.github/skills/*/SKILL.md` is owned by whichever specialized agent declares it (see that agent's `.agent.md`). When acting as the master/orchestrator, delegate to that specialist instead of invoking the skill directly yourself. Only use a skill directly if no specialist owns that domain.
4. **Auto-create reusable skills.** If you complete a multi-step task that is costly (≥3 tool calls or likely to repeat) and is not yet covered by an existing instructions/prompt file, propose creating one:
   - Domain-scoped conventions that should apply automatically whenever matching files are edited → new file in `.github/instructions/<topic>.instructions.md` with an `applyTo` glob (see existing ones for the pattern).
   - On-demand multi-step workflows invoked by name → new file in `.github/prompts/<name>.prompt.md`.
   - Keep agent definitions in `.github/agents/` only; the Maestro server reads them from there. When adding or renaming an agent, update `SKILL_OWNER` / `WORKFLOW_AGENTS` in `agent/2_orchestrator/workflows.py` (guarded by `agent/tests/`).
5. **Keep it portable.** Prefer `AGENTS.md`-style plain instructions over VS Code-only mechanisms when possible, since other tools (e.g. Claude Code) may read this repo later.

---

## 🏗️ Architecture

```
agent/
├── 1_interface/    MCP server (tools + agent prompts), agent registry, CV backend adapter
├── 2_orchestrator/ Workflow catalog + maestro (agent -> skill plan and execution)
├── 4_skills/       11 command skills (pnpm/uv/git/gh), see agent/README.md
└── tests/          pytest guards for agents, skills and workflows

apps/
├── web/           React + TypeScript + Tailwind + Vite + Playwright
└── api/           FastAPI (Python) + Pytest

packages/          Shared code (core, ui, api-client, config)
```

---

## 🧹 Project structure hygiene (enforced)

- Never commit runtime artifacts: logs (`*.log`, `*.err`), `output.txt`, `summary.txt`, coverage/, dist/, playwright-report/, test-results/, `.venv/`, `.state/`, `.checkpoints/`. These must stay gitignored.
- Reusable setup/verification/maintenance scripts belong in `scripts/` (see `scripts/README.md`), never loose at the repo root. Repo-root `.ps1`/`.sh` files are only acceptable if they are one-off, throwaway, and never committed.
- The `agent/` root only holds `pyproject.toml`, `uv.lock` and `README.md`. Runtime logic lives in the numbered layer folders (`1_interface/`, `2_orchestrator/`, `4_skills/`) and tests in `agent/tests/`.
- **Never create markdown documentation directly at the repo root.** Follow `docs/DOCUMENTATION_GUIDE.md`:
  - End-user/external docs → `docs/` (e.g. `docs/QUICK_START.md`, `docs/SETUP.md`, `docs/MAESTRO_REFERENCE.md`).
  - Internal analysis, session summaries, phase reports → `.dev-docs/` (e.g. `.dev-docs/architecture/`, `.dev-docs/sessions/`).
  - Agent/skill configuration → `.agent/` (only files with agent/skill frontmatter, not prose reports).
  - The only markdown allowed at repo root is `README.md` and a short `QUICK_START.md` stub that links to `docs/QUICK_START.md`.
- Before finishing a task that adds new top-level files, verify they match this structure. If a new file doesn't fit an existing layer/folder, ask where it should go instead of defaulting to the repo root.
- When moving/renaming a doc, grep the repo for old references (other docs, scripts, `.github/agents/*.agent.md`) and update them so links don't break.

---

## 🚀 Workflows (maestro MCP)

Preview with `maestro-plan`, run with `maestro` (stops at the first failing skill).

| Workflow | What it does |
|----------|-------------|
| `ci` | Install → type-check → unit + backend tests → build |
| `test` | Unit + backend tests → E2E → coverage |
| `deploy` | Quality gate → build + latest Pages deploy run (Pages deploys from `deploy.yml` on main) |
| `portfolio-update` | CV backend in sync + web reads it → unit tests |
| `quality` | Type-check → coverage → quality gate |
| `full-pipeline` | Install, quality gate, E2E, CV sync, branch/PR status, Pages build |

---

## 🔧 Commands

```bash
# Maestro agent tests
uv run --project agent python -m pytest agent/tests -q

# Web frontend (apps/web/)
pnpm -F @mportafolio/web dev
pnpm -F @mportafolio/web test
pnpm -F @mportafolio/web lint     # tsc --noEmit
pnpm -F @mportafolio/web build

# API backend (apps/api/)
cd apps/api && uv run pytest
cd apps/api && uv run python run.py
```

---

## 📋 Code Conventions

### Python (agent/, apps/api/, packages/backend/)
- **Version**: Python 3.11–3.12
- **Package manager**: `uv` (NOT pip, NOT poetry)
- **Framework**: MCP SDK (agent), FastAPI (API)
- **Testing**: pytest
- **Typing**: Full type hints required
- **Path handling**: Always use `pathlib.Path`, never string concatenation
- **Logging**: `logging.getLogger(__name__)`; the MCP server logs to stderr (stdout is the protocol channel)
- **Skills**: New skills subclass `CommandSkill` (`agent/4_skills/base_skill.py`) and declare `STEPS` from `repo_commands.py`
- **Subprocesses**: Skills run commands only through `BaseSkill.run_command()`

### TypeScript (apps/web/, packages/)
- **Version**: TypeScript 5.x strict mode
- **Package manager**: `pnpm` (NOT npm, NOT yarn)
- **Framework**: React 19 + Vite + Tailwind CSS
- **Testing**: Vitest (unit) + Playwright (E2E)
- **Linting**: ESLint + Prettier (config in `packages/config/`)
- **Components**: Functional components only, no class components
- **State**: useState/useReducer for local, context for shared
- **Imports**: Use absolute paths with `@/` prefix (configured in tsconfig)

---

## 🛡️ Security Rules (NEVER violate these)

1. **NEVER** build shell strings in agent code — skills pass argument lists to `BaseSkill.run_command()`
2. **NEVER** commit secrets — use env vars from `.env` (local) or GitHub Secrets (CI/CD)
3. **NEVER** modify `.github/workflows/` without running tests first
4. **NEVER** push to `main` directly — always use PRs with passing CI
5. **NEVER** pass user-provided input to the filesystem or a subprocess unvalidated (e.g. `cv-apply` only accepts plain `.md`/`.txt` names)

---

## 🎯 Agent Hierarchy

```
@maestro (agent-master-portfolio)
├── portfolio-cv-manager       → cv-* tools + cv_sync_checker
├── portfolio-test-manager     → e2e_test_runner
├── portfolio-deployment-manager → github_pages_deployer
├── github-cicd-manager        → git_workflow_manager + release_orchestrator
├── setup-portability-manager  → setup/bootstrapping + MCP validation
├── devops-cicd-manager        → CI/CD engineering and release governance
├── software-architecture-manager → architecture and ADR governance
├── sdet-quality-manager       → web/api/mobile test strategy
├── platform-architecture-manager → Docker/K8s runtime architecture
└── os-platform-manager        → Linux/Windows environment parity
```

---

## 🧩 Custom Prompts & Local Knowledge

Prompt files for specialist behaviors are stored in `.github/prompts/`:
- `devops.prompt.md`
- `architect.prompt.md`
- `sdet.prompt.md`
- `platform.prompt.md`
- `sysops.prompt.md`
- `self-heal-loop.prompt.md`

Workspace grounding context for local indexing/RAG is stored in `.github/agents/context/`:
- `monorepo-map.md`
- `api-contracts.md`
- `testing-matrix.md`
- `platform-topology.md`
- `os-compatibility.md`
- `compliance-matrix.md`

Before major changes, consult these context files first to reduce hallucinations and enforce architecture consistency.

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `.vscode/mcp.json` · `.cursor/mcp.json` · `.mcp.json` | `maestro` MCP registration for VS Code · Cursor · Claude Code |
| `.github/agents/*.agent.md` | Custom Agents: master + 10 specialized agent definitions (workspace-scoped, auto-appear in the agent picker) |
| `.github/instructions/*.instructions.md` | Generic per-role skills, auto-applied by `applyTo` glob |
| `.github/prompts/*.prompt.md` | On-demand multi-step workflows, invoked via `/name` |
| `agent/1_interface/mcp_server.py` | MCP server (IDE connector: tools + agent prompts) |
| `agent/1_interface/agent_registry.py` | Reads `.github/agents` for the MCP server (`maestro-context`, `maestro-agent`) |
| `agent/2_orchestrator/workflows.py` | Workflow → skills, skill → owner agent, workflow → agent order |
| `agent/2_orchestrator/maestro.py` | Builds and runs the agent → skill plan |
| `agent/4_skills/base_skill.py` | `BaseSkill` / `CommandSkill` / `SkillResult` |
| `agent/4_skills/skill_registry.py` | Skill name → class |

---

## 🔁 Feedback Loop (Self-Correction)

When a skill fails:
1. It returns `status: failed|timeout` with the failing step, its command, exit code and output tail in `errors[]`
2. `maestro` stops the workflow there and returns every stage run so far
3. Fix the cause, re-run that `skill-*` tool, then the workflow

**Skills return a structured `SkillResult` — they raise `SkillFailed` internally, never to the caller.**

---

## 🧪 Testing Protocol

Before any PR:
```bash
# Agent + CV backend tests
uv run --project agent python -m pytest agent/tests -q
pnpm test:backend

# Frontend type-check, unit and E2E tests
pnpm -F @mportafolio/web lint
pnpm -F @mportafolio/web exec vitest run
pnpm -F @mportafolio/web test:e2e

# Or everything CI runs, via MCP: skill-release-orchestrator
```

---

## 💡 Common 1-line Prompts

```
"Agente: ejecuta el pipeline completo y repara si falla"
"@maestro workflow: ci"
"@maestro workflow: deploy"
"Skill: run E2E tests on chromium only"
"@maestro workflow: portfolio-update"
```
