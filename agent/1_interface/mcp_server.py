#!/usr/bin/env python3
"""
Maestro MCP server (Model Context Protocol, stdio).

Protocol adapter only: exposes the session tools, the CV backend tools, the maestro workflows and
the skills as MCP tools, and every `.github/agents/*.agent.md` definition as an MCP prompt.

Usage:
    uv run --directory agent python 1_interface/mcp_server.py
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequestParams,
    CallToolResult,
    GetPromptRequestParams,
    GetPromptResult,
    ListPromptsResult,
    ListToolsResult,
    PaginatedRequestParams,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
)

# Numbered layer folders are not importable packages, so each layer goes on sys.path.
_AGENT_ROOT = Path(__file__).resolve().parent.parent
for _layer in ("4_skills", "2_orchestrator", "1_interface"):
    sys.path.insert(0, str(_AGENT_ROOT / _layer))

import agent_registry  # noqa: E402
import cv_pipeline  # noqa: E402
import maestro  # noqa: E402
import skill_registry  # noqa: E402
import workflows  # noqa: E402

logger = logging.getLogger("maestro")
server = Server("maestro")

EXPOSED_SKILLS: List[str] = [
    "type_checker",
    "unit_test_runner",
    "e2e_test_runner",
    "build_orchestrator",
    "quality_gate_runner",
    "coverage_analyzer",
    "cv_sync_checker",
    "github_pages_deployer",
    "release_orchestrator",
    "git_workflow_manager",
]

_EMPTY_SCHEMA: Dict[str, Any] = {"type": "object", "properties": {}}
_SKILL_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {"verbose": {"type": "boolean", "description": "Include the output of passing steps"}},
}


def _workflow_schema(description: str, with_options: bool) -> Dict[str, Any]:
    properties: Dict[str, Any] = {
        "workflow": {"type": "string", "enum": list(workflows.WORKFLOW_SKILLS), "description": description},
    }
    if with_options:
        properties["options"] = {
            "type": "object",
            "properties": {
                "continue_on_error": {"type": "boolean", "description": "Run the remaining skills after a failure"},
                "verbose": {"type": "boolean", "description": "Include the output of passing steps"},
            },
        }
    return {"type": "object", "properties": properties, "required": ["workflow"]}


def get_tools() -> List[Tool]:
    agent_names = sorted(agent_registry.load_agents())
    session_and_cv = [
        Tool(
            name="maestro-context",
            description=(
                "[START HERE] Call once at the start of every session in mi-portafolio. Returns the session protocol, "
                "all .github/agents with their workflows/skills/MCP tools, key repo paths (CV pipeline) and "
                "agent<->maestro consistency issues."
            ),
            inputSchema=_EMPTY_SCHEMA,
        ),
        Tool(
            name="maestro-agent",
            description="[AGENT] Load a .github/agents definition (instructions, owned skills, MCP tools) to act as that agent",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent": {"type": "string", "enum": agent_names, "description": "Agent name"},
                    "task": {"type": "string", "description": "Optional task to append to the agent prompt"},
                },
                "required": ["agent"],
            },
        ),
        Tool(
            name="cv-status",
            description=(
                "[CV] CV backend status: are cv/output Word/PDF and cv-data.json (web data) rendered from the "
                "same CV, and which change requests wait in cv/input/requests"
            ),
            inputSchema=_EMPTY_SCHEMA,
        ),
        Tool(
            name="cv-apply",
            description=(
                "[CV] Apply a CV change request with the Python backend and regenerate Word/PDF + web data. "
                "Pass `content` (the .md request written from the user's chat instructions, format in "
                "cv/input/request-template.md), or `request_path` (a .md/.txt the user points to). "
                "With no arguments, applies every pending file in cv/input/requests."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Request in the template format (## Curso, - titulo: ...)"},
                    "filename": {"type": "string", "description": "Name for `content`, e.g. 2026-09-docker.md"},
                    "request_path": {"type": "string", "description": "Repo-relative or absolute .md/.txt request"},
                },
            },
        ),
        Tool(
            name="cv-generate",
            description="[CV] Re-render cv/output Word/PDF and cv-data.json from the current CV (no data changes)",
            inputSchema=_EMPTY_SCHEMA,
        ),
    ]
    orchestration = [
        Tool(
            name="maestro",
            description="[MAESTRO] Run a workflow: its skills in order, stopping at the first failure",
            inputSchema=_workflow_schema("Workflow to run", with_options=True),
        ),
        Tool(
            name="maestro-plan",
            description="[PLAN] Preview a workflow (owning agents and skill sequence) without running it",
            inputSchema=_workflow_schema("Workflow to preview", with_options=False),
        ),
    ]
    skills = [
        Tool(
            name=agent_registry.skill_tool_name(name),
            description=skill_registry.SKILLS[name].DESCRIPTION,
            inputSchema=_SKILL_SCHEMA,
        )
        for name in EXPOSED_SKILLS
    ]
    return session_and_cv + orchestration + skills


def _agent_views() -> tuple[dict, list[str]]:
    agents = agent_registry.load_agents()
    exposed = [tool.name for tool in get_tools()]
    views = agent_registry.build_views(agents, workflows.SKILL_OWNER, workflows.WORKFLOW_AGENTS, exposed)
    issues = agent_registry.consistency_issues(agents, workflows.SKILL_OWNER, workflows.WORKFLOW_AGENTS)
    return views, issues


def handle_maestro_context(_arguments: dict) -> dict:
    views, issues = _agent_views()
    return agent_registry.build_context(views, workflows.WORKFLOW_AGENTS, issues)


def handle_maestro_agent(arguments: dict) -> dict:
    name = arguments.get("agent", "")
    views, _ = _agent_views()
    view = views.get(name)
    if view is None:
        return {"status": "error", "error": f"Unknown agent '{name}'", "available": sorted(views)}
    return {"status": "success", **view.detail(), "prompt": agent_registry.render_agent_prompt(view, arguments.get("task", ""))}


def handle_maestro(arguments: dict) -> dict:
    options = arguments.get("options") or {}
    return maestro.run_workflow(
        arguments.get("workflow", ""),
        continue_on_error=bool(options.get("continue_on_error", False)),
        verbose=bool(options.get("verbose", False)),
    )


def handle_maestro_plan(arguments: dict) -> dict:
    return maestro.describe(arguments.get("workflow", ""))


def _skill_handler(name: str) -> Callable[[dict], dict]:
    return lambda arguments: maestro.run_skill(name, verbose=bool(arguments.get("verbose", False)))


HANDLERS: Dict[str, Callable[[dict], dict]] = {
    "maestro-context": handle_maestro_context,
    "maestro-agent": handle_maestro_agent,
    "cv-status": cv_pipeline.cv_status,
    "cv-apply": cv_pipeline.cv_apply,
    "cv-generate": cv_pipeline.cv_generate,
    "maestro": handle_maestro,
    "maestro-plan": handle_maestro_plan,
    **{agent_registry.skill_tool_name(name): _skill_handler(name) for name in EXPOSED_SKILLS},
}


def _text(payload: dict) -> CallToolResult:
    return CallToolResult(content=[TextContent(type="text", text=json.dumps(payload, ensure_ascii=False))])


async def handle_list_tools(_ctx: Any, _params: PaginatedRequestParams) -> ListToolsResult:
    return ListToolsResult(tools=get_tools())


async def handle_call_tool(_ctx: Any, params: CallToolRequestParams) -> CallToolResult:
    handler = HANDLERS.get(params.name)
    if handler is None:
        return _text({"status": "error", "error": f"Tool '{params.name}' not found"})
    logger.info("tool %s", params.name)
    try:
        # Skills block on subprocesses for minutes; keep the stdio loop responsive.
        return _text(await asyncio.to_thread(handler, params.arguments or {}))
    except Exception as exc:
        logger.exception("tool %s failed", params.name)
        return _text({"status": "error", "error": str(exc)})


async def handle_list_prompts(_ctx: Any, _params: PaginatedRequestParams) -> ListPromptsResult:
    agents = agent_registry.load_agents()
    return ListPromptsResult(prompts=[
        Prompt(
            name=spec.name,
            description=spec.description,
            arguments=[PromptArgument(name="task", description=spec.argument_hint or "Task for the agent", required=False)],
        )
        for spec in agents.values()
    ])


async def handle_get_prompt(_ctx: Any, params: GetPromptRequestParams) -> GetPromptResult:
    views, _ = _agent_views()
    view = views.get(params.name)
    if view is None:
        raise ValueError(f"Unknown agent prompt '{params.name}'")
    task = (params.arguments or {}).get("task", "")
    return GetPromptResult(
        description=view.spec.description,
        messages=[PromptMessage(role="user", content=TextContent(type="text", text=agent_registry.render_agent_prompt(view, task)))],
    )


async def main() -> None:
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")
    # MCP SDK 2.x: params_type must be a RequestParams model and handlers receive (ctx, params)
    server.add_request_handler("tools/list", PaginatedRequestParams, handle_list_tools)
    server.add_request_handler("tools/call", CallToolRequestParams, handle_call_tool)
    server.add_request_handler("prompts/list", PaginatedRequestParams, handle_list_prompts)
    server.add_request_handler("prompts/get", GetPromptRequestParams, handle_get_prompt)
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Maestro MCP server ready on stdio")
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
