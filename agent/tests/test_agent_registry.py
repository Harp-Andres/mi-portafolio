"""Guards the two-way link between .github/agents and the maestro MCP server."""

import asyncio
import json
import re

import pytest
from mcp.types import CallToolRequestParams, GetPromptRequestParams, PaginatedRequestParams

import agent_registry
import cv_pipeline
import workflows


@pytest.fixture(scope="module")
def server():
    import mcp_server

    return mcp_server


def test_agents_are_discovered():
    agents = agent_registry.load_agents()
    assert agent_registry.MASTER_AGENT in agents
    assert len(agents) >= 11
    assert all(spec.description for spec in agents.values())


def test_agents_and_maestro_are_consistent():
    agents = agent_registry.load_agents()
    issues = agent_registry.consistency_issues(agents, workflows.SKILL_OWNER, workflows.WORKFLOW_AGENTS)
    assert issues == []


def test_every_agent_participates_in_a_workflow(server):
    views, _ = server._agent_views()
    assert [name for name, view in views.items() if not view.workflows] == []


def test_context_tool_returns_protocol_and_paths(server):
    params = CallToolRequestParams(name="maestro-context", arguments={})
    result = asyncio.run(server.handle_call_tool(None, params))
    payload = json.loads(result.content[0].text)
    assert payload["status"] == "success"
    assert payload["protocol"]
    assert payload["paths"]["cv_requests"].startswith("cv/input/requests/")
    assert payload["paths"]["cv_web_data"].startswith("cv/output/cv-data.json")
    assert {a["name"] for a in payload["agents"]} >= {"portfolio-cv-manager", agent_registry.MASTER_AGENT}


def test_agent_tool_returns_instructions(server):
    params = CallToolRequestParams(name="maestro-agent", arguments={"agent": "portfolio-cv-manager", "task": "add a course"})
    payload = json.loads(asyncio.run(server.handle_call_tool(None, params)).content[0].text)
    assert payload["status"] == "success"
    assert "portfolio-update" in payload["workflows"]
    assert "Task: add a course" in payload["prompt"]


def test_agents_are_exposed_as_prompts(server):
    listed = asyncio.run(server.handle_list_prompts(None, PaginatedRequestParams()))
    assert {p.name for p in listed.prompts} == set(agent_registry.load_agents())
    prompt = asyncio.run(
        server.handle_get_prompt(None, GetPromptRequestParams(name="portfolio-test-manager", arguments={"task": "fix e2e"}))
    )
    assert "maestro-context" in prompt.messages[0].content.text


def test_tool_list_includes_session_tools(server):
    listed = asyncio.run(server.handle_list_tools(None, PaginatedRequestParams()))
    names = [tool.name for tool in listed.tools]
    assert names[:5] == ["maestro-context", "maestro-agent", "cv-status", "cv-apply", "cv-generate"]


def test_agent_files_list_their_real_maestro_tools(server):
    views, _ = server._agent_views()
    for name, view in views.items():
        match = re.search(r"Your maestro tools: (.*?)\. Re-check", view.spec.instructions)
        if match is None:
            continue
        listed = re.findall(r"`([\w-]+)`", match.group(1).split("—")[0])
        expected = [] if "no dedicated" in match.group(1) else view.mcp_tools
        assert sorted(listed) == sorted(expected), f"{view.spec.path}: lists {listed}, maestro exposes {view.mcp_tools}"


def test_cv_manager_owns_cv_tools(server):
    views, _ = server._agent_views()
    assert views["portfolio-cv-manager"].mcp_tools[:3] == ["cv-status", "cv-apply", "cv-generate"]


def _call(server, name, arguments):
    return json.loads(asyncio.run(server.handle_call_tool(None, CallToolRequestParams(name=name, arguments=arguments))).content[0].text)


def test_cv_status_comes_from_the_backend_and_is_in_sync(server):
    payload = _call(server, "cv-status", {})
    assert payload["status"] == "success", payload
    assert payload["inSync"] is True, payload
    assert len(payload["documents"]) == 4


def test_cv_apply_reports_backend_errors_without_changing_the_cv(server, tmp_path):
    state = cv_pipeline.REPO_ROOT / "cv" / "output" / "cv-data.json"
    before = state.read_bytes()
    bad_request = tmp_path / "bad.md"
    bad_request.write_text("## Vacaciones\n- dias: 3\n", encoding="utf-8")
    payload = _call(server, "cv-apply", {"request_path": str(bad_request)})
    assert payload["status"] == "failed"
    assert "Unknown section" in payload["output"]
    assert state.read_bytes() == before
    assert _call(server, "cv-apply", {"content": "x", "filename": "../evil.md"})["status"] == "error"
