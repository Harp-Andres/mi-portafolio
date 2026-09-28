"""Unit, E2E and coverage runs."""

import repo_commands as cmd
from base_skill import CommandSkill


class UnitTestRunner(CommandSkill):
    NAME = "unit_test_runner"
    DESCRIPTION = "[TEST] Web unit tests (Vitest) and CV backend tests (pytest)"
    STEPS = (cmd.WEB_UNIT_TESTS, cmd.BACKEND_TESTS)


class E2ETestRunner(CommandSkill):
    NAME = "e2e_test_runner"
    DESCRIPTION = "[PLAY] Web E2E tests (Playwright, Chromium)"
    STEPS = (cmd.WEB_E2E,)


class CoverageAnalyzer(CommandSkill):
    NAME = "coverage_analyzer"
    DESCRIPTION = "[COVERAGE] Web unit tests with the V8 coverage report"
    STEPS = (cmd.WEB_COVERAGE,)
