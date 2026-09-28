"""Install, type-check, build and the combined quality gate."""

import repo_commands as cmd
from base_skill import CommandSkill


class DependencyResolver(CommandSkill):
    NAME = "dependency_resolver"
    DESCRIPTION = "[DEPS] Install the pnpm workspace exactly as locked (pnpm install --frozen-lockfile)"
    STEPS = (cmd.INSTALL,)


class TypeChecker(CommandSkill):
    NAME = "type_checker"
    DESCRIPTION = "[CHECK] TypeScript check of the web app (pnpm -F @mportafolio/web lint = tsc --noEmit)"
    STEPS = (cmd.WEB_TYPECHECK,)


class BuildOrchestrator(CommandSkill):
    NAME = "build_orchestrator"
    DESCRIPTION = "[BUILD] Production build of the web app (syncs CV downloads, tsc, vite build)"
    STEPS = (cmd.WEB_BUILD,)


class QualityGateRunner(CommandSkill):
    NAME = "quality_gate_runner"
    DESCRIPTION = "[GATE] Type-check, web unit tests, CV backend tests and build, stopping at the first failure"
    STEPS = (cmd.WEB_TYPECHECK, cmd.WEB_UNIT_TESTS, cmd.BACKEND_TESTS, cmd.WEB_BUILD)
