# Maestro agent

MCP server that links the agents in `.github/agents/` with the repo skills and the CV backend (`apps/api`).
Cursor (`.cursor/mcp.json`), VS Code (`.vscode/mcp.json`) and Claude Code (`.mcp.json`) start it with:

```bash
uv run --directory agent python 1_interface/mcp_server.py
```

Enable the `maestro` server once in the IDE (Cursor: Settings → MCP). Requirements: Python 3.11+, `uv`, `pnpm`,
and an authenticated `gh` CLI for the GitHub skills.

## Layers

Numbered folders are not Python packages; the server (and `tests/conftest.py`) puts each layer on `sys.path`.

| Layer | Module | Responsibility |
| --- | --- | --- |
| `1_interface/` | `mcp_server.py` | MCP protocol adapter: tool catalog, dispatch, agent prompts |
| | `agent_registry.py` | Reads `.github/agents/*.agent.md` and checks agent ↔ maestro consistency |
| | `cv_pipeline.py` | `cv-status` / `cv-apply` / `cv-generate` over `python -m app` (apps/api) |
| `2_orchestrator/` | `workflows.py` | Workflow → skills, skill → owning agent, workflow → agent order |
| | `maestro.py` | Builds the agent → skill plan and runs a workflow |
| `4_skills/` | `base_skill.py` | `BaseSkill`, `CommandSkill` (runs declared `Step`s), `SkillResult` |
| | `repo_commands.py` | The pnpm / uv / git / gh commands, mirroring `.github/workflows/deploy.yml` |
| | `*_skills.py` | One class per skill, grouped by domain |
| | `skill_registry.py` | Name → skill class |

## MCP tools

| Tool | What it does |
| --- | --- |
| `maestro-context` | Session start: protocol, agents with their workflows/skills/tools, key paths, consistency issues |
| `maestro-agent` | Instructions of one agent (also exposed as MCP prompts) |
| `cv-status`, `cv-apply`, `cv-generate` | CV backend: sync status, apply a change request, re-render Word/PDF + web JSON |
| `maestro-plan` | Preview a workflow |
| `maestro` | Run a workflow, stopping at the first failing skill (`options.continue_on_error` to keep going) |
| `skill-*` | Run one skill (`verbose` adds the output of passing steps) |

## Skills and workflows

| Skill | Runs | Owner |
| --- | --- | --- |
| `dependency_resolver` | `pnpm install --frozen-lockfile` | devops-cicd-manager |
| `type_checker` | `pnpm -F @mportafolio/web lint` | software-architecture-manager |
| `build_orchestrator` | `pnpm -F @mportafolio/web build` | devops-cicd-manager |
| `quality_gate_runner` | type-check → web unit → backend tests → build | devops-cicd-manager |
| `unit_test_runner` | `vitest run` + `pnpm test:backend` | sdet-quality-manager |
| `e2e_test_runner` | `pnpm -F @mportafolio/web test:e2e` | portfolio-test-manager |
| `coverage_analyzer` | `vitest run --coverage` | sdet-quality-manager |
| `cv_sync_checker` | CV backend status (no pending requests, in sync) + `pnpm sync:verify` | portfolio-cv-manager |
| `git_workflow_manager` | `git status --short --branch` + `gh pr status` | github-cicd-manager |
| `github_pages_deployer` | web build + latest `deploy.yml` run on main (never pushes) | portfolio-deployment-manager |
| `release_orchestrator` | every CI check locally before merging | github-cicd-manager |

| Workflow | Skills |
| --- | --- |
| `ci` | dependency_resolver, type_checker, unit_test_runner, build_orchestrator |
| `test` | unit_test_runner, e2e_test_runner, coverage_analyzer |
| `deploy` | quality_gate_runner, github_pages_deployer |
| `portfolio-update` | cv_sync_checker, unit_test_runner |
| `quality` | type_checker, coverage_analyzer, quality_gate_runner |
| `full-pipeline` | dependency_resolver, quality_gate_runner, e2e_test_runner, cv_sync_checker, git_workflow_manager, github_pages_deployer |

GitHub Pages is only deployed by `.github/workflows/deploy.yml` on push to `main`.

## Adding a skill

1. Add the command to `repo_commands.py` if it is new.
2. Add a `CommandSkill` subclass with `NAME`, `DESCRIPTION` and `STEPS` to the matching `*_skills.py`
   (override `_run` only when the result needs parsing, as `CvSyncChecker` does).
3. Register it in `skill_registry.SKILLS`, give it an owner in `workflows.SKILL_OWNER` and, if it should be an
   MCP tool, add it to `mcp_server.EXPOSED_SKILLS`.

`tests/test_skills.py` fails if a skill is unregistered, has no owner, or a workflow references an unknown skill;
`tests/test_agent_registry.py` fails if an agent referenced here is missing from `.github/agents/`.

## Tests

```bash
uv run --project agent python -m pytest agent/tests -q
```

Behind a TLS-intercepting proxy set `UV_SYSTEM_CERTS=1` first.
