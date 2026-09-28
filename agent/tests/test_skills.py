"""Skills, workflow catalog and maestro orchestration, without running the real repo commands."""

import json
import subprocess
import sys

import pytest

import agent_registry
import maestro
import skill_registry
import workflows
from base_skill import CommandSkill, SkillRequest, SkillStatus, Step
from cv_skills import CvSyncChecker

PYTHON = sys.executable


def _step(label: str, code: str, timeout: int = 60) -> Step:
    return Step(label, (PYTHON, "-c", code), timeout=timeout)


def _skill(*steps: Step) -> CommandSkill:
    skill_class = type("FakeSkill", (CommandSkill,), {"NAME": "fake", "DESCRIPTION": "fake", "STEPS": steps})
    return skill_class()


@pytest.mark.parametrize("name", sorted(skill_registry.SKILLS))
def test_every_registered_skill_instantiates(name):
    skill = skill_registry.create_skill(name)
    assert skill.NAME == name
    assert skill.DESCRIPTION


def test_unknown_skill_is_rejected():
    with pytest.raises(KeyError, match="Unknown skill"):
        skill_registry.create_skill("pdf_generator")


def test_every_workflow_skill_is_registered_and_owned():
    agents = agent_registry.load_agents()
    for workflow, skills in workflows.WORKFLOW_SKILLS.items():
        assert set(skills) <= set(skill_registry.SKILLS), workflow
    assert set(workflows.SKILL_OWNER) == set(skill_registry.SKILLS)
    assert set(workflows.SKILL_OWNER.values()) <= set(agents)
    assert set(workflows.WORKFLOW_AGENTS) == set(workflows.WORKFLOW_SKILLS)


def test_server_exposes_only_registered_skills():
    import mcp_server

    assert set(mcp_server.EXPOSED_SKILLS) <= set(skill_registry.SKILLS)
    tools = {tool.name: tool for tool in mcp_server.get_tools()}
    for name in mcp_server.EXPOSED_SKILLS:
        assert tools[agent_registry.skill_tool_name(name)].description == skill_registry.SKILLS[name].DESCRIPTION


def test_command_skill_runs_every_step():
    result = _skill(_step("first", "print('one')"), _step("second", "print('two')")).execute(SkillRequest(verbose=True))
    assert result.success
    assert result.output.splitlines() == ["PASS first", "one", "PASS second", "two"]


def test_command_skill_stops_at_the_first_failing_step():
    result = _skill(_step("broken", "import sys; print('boom'); sys.exit(3)"), _step("never", "print('x')")).execute()
    assert result.status is SkillStatus.FAILED
    assert "FAIL broken" in result.errors[0] and "exited with 3" in result.errors[0] and "boom" in result.errors[0]
    assert "never" not in result.errors[0]


def test_command_skill_reports_a_missing_tool():
    result = _skill(Step("missing", ("definitely-not-a-real-tool-xyz",))).execute()
    assert result.status is SkillStatus.FAILED


def test_command_skill_reports_timeouts():
    result = _skill(_step("slow", "import time; time.sleep(5)", timeout=1)).execute()
    assert result.status is SkillStatus.TIMEOUT
    assert "timed out after 1s" in result.errors[0]


def test_plan_groups_skills_by_owner_in_agent_order():
    plan = maestro.build_plan("portfolio-update")
    assert plan == [
        {"agent": "portfolio-cv-manager", "skills": ["cv_sync_checker"]},
        {"agent": "sdet-quality-manager", "skills": ["unit_test_runner"]},
    ]
    assert maestro.describe("nope")["status"] == "failed"


def test_workflow_stops_at_the_first_failed_skill(monkeypatch):
    passing = type("Passing", (CommandSkill,), {"NAME": "passing", "DESCRIPTION": "ok", "STEPS": (_step("ok", "pass"),)})
    failing = type("Failing", (CommandSkill,), {"NAME": "failing", "DESCRIPTION": "ko", "STEPS": (_step("ko", "raise SystemExit(1)"),)})
    monkeypatch.setitem(skill_registry.SKILLS, "passing", passing)
    monkeypatch.setitem(skill_registry.SKILLS, "failing", failing)
    monkeypatch.setitem(workflows.WORKFLOW_SKILLS, "fake", ["passing", "failing", "passing"])

    report = maestro.run_workflow("fake")
    assert report["status"] == "failed"
    assert [stage["skill"] for stage in report["stages"]] == ["passing", "failing"]

    report = maestro.run_workflow("fake", continue_on_error=True)
    assert [stage["success"] for stage in report["stages"]] == [True, False, True]


class _FakeCvChecker(CvSyncChecker):
    def __init__(self, status: dict):
        super().__init__()
        self.status = status
        self.commands = []

    def run_command(self, command, timeout=600):
        self.commands.append(command)
        stdout = json.dumps(self.status) if "status" in command else ""
        return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")


@pytest.mark.parametrize(
    ("status", "error"),
    [
        ({"pendingRequests": ["cv/input/requests/x.md"], "inSync": True}, "Pending CV requests"),
        ({"pendingRequests": [], "inSync": False}, "out of sync"),
    ],
)
def test_cv_sync_checker_fails_before_the_web_check(status, error):
    checker = _FakeCvChecker(status)
    result = checker.execute()
    assert result.status is SkillStatus.FAILED
    assert error in result.errors[0]
    assert len(checker.commands) == 1


def test_cv_sync_checker_passes_when_backend_and_web_agree():
    checker = _FakeCvChecker({"pendingRequests": [], "inSync": True})
    result = checker.execute()
    assert result.success
    assert checker.commands[-1] == ("pnpm", "sync:verify")
