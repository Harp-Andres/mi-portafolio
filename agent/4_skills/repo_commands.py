"""Repo commands shared by the skills; they mirror the jobs of .github/workflows/deploy.yml."""

from base_skill import Step

WEB = "@mportafolio/web"

INSTALL = Step("Install dependencies", ("pnpm", "install", "--frozen-lockfile"))
WEB_TYPECHECK = Step("TypeScript check", ("pnpm", "-F", WEB, "lint"))
WEB_UNIT_TESTS = Step("Web unit tests", ("pnpm", "-F", WEB, "exec", "vitest", "run"))
WEB_COVERAGE = Step("Web unit tests with coverage", ("pnpm", "-F", WEB, "exec", "vitest", "run", "--coverage"), show_output=True)
WEB_E2E = Step("Web E2E tests", ("pnpm", "-F", WEB, "test:e2e"), timeout=1800)
WEB_BUILD = Step("Web build", ("pnpm", "-F", WEB, "build"))
BACKEND_TESTS = Step("CV backend tests", ("pnpm", "test:backend"))
CV_WEB_SYNC = Step("Web reads the current CV", ("pnpm", "sync:verify"))
CV_STATUS = Step("CV backend status", ("uv", "run", "--project", "apps/api", "python", "-m", "app", "status", "--json"))

LATEST_MAIN_DEPLOY = Step(
    "Latest GitHub Pages deploy on main",
    ("gh", "run", "list", "--workflow", "deploy.yml", "--branch", "main", "--limit", "1"),
    show_output=True,
)
BRANCH_STATUS = Step("Branch status", ("git", "status", "--short", "--branch"), show_output=True)
PULL_REQUESTS = Step("Pull requests", ("gh", "pr", "status"), show_output=True)
