#!/usr/bin/env python3
"""
MCP Server - Maestro Agent

Exposes maestro orchestrator and portfolio skills as MCP tools, and every
`.github/agents/*.agent.md` definition as an MCP prompt (see agent_registry.py).
Implements Model Context Protocol 2.2.0

Usage:
    python 1_interface/mcp_server.py
"""

import asyncio
import inspect
import json
import sys
from pathlib import Path
from typing import Any

# MCP imports
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

# Setup path
_AGENT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_AGENT_ROOT))
sys.path.insert(0, str(Path(__file__).parent))

import agent_registry  # noqa: E402
import cv_pipeline  # noqa: E402

WORKFLOWS = ["ci", "test", "deploy", "portfolio-update", "quality", "full-pipeline"]


def get_logger(name: str):
    """Simple logger without circular dependency issues"""
    import logging
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


logger = get_logger("mcp_server")

# Create MCP server
server = Server("maestro")


_handlers_mod = None


def _load_handlers():
    """Load handlers.py by path (numbered directories are not importable packages)."""
    global _handlers_mod
    if _handlers_mod is None:
        import importlib.util as _ilu
        spec = _ilu.spec_from_file_location("handlers", _AGENT_ROOT / "1_interface" / "handlers.py")
        _handlers_mod = _ilu.module_from_spec(spec)
        spec.loader.exec_module(_handlers_mod)
    return _handlers_mod


def _agent_views() -> tuple[dict, list[str]]:
    handlers_mod = _load_handlers()
    agents = agent_registry.load_agents()
    exposed = [tool.name for tool in get_tools()]
    views = agent_registry.build_views(
        agents, handlers_mod.SKILL_SPECIALIZED_OWNER, handlers_mod.WORKFLOW_AGENT_PRIORITY, exposed
    )
    issues = agent_registry.consistency_issues(
        agents, handlers_mod.SKILL_SPECIALIZED_OWNER, handlers_mod.WORKFLOW_AGENT_PRIORITY
    )
    return views, issues


def handle_maestro_context(_arguments: dict) -> dict:
    views, issues = _agent_views()
    return agent_registry.build_context(views, _load_handlers().WORKFLOW_AGENT_PRIORITY, issues)


def handle_maestro_agent(arguments: dict) -> dict:
    name = arguments.get("agent", "")
    views, _ = _agent_views()
    view = views.get(name)
    if view is None:
        return {"status": "error", "error": f"Unknown agent '{name}'", "available": sorted(views)}
    return {"status": "success", **view.detail(), "prompt": agent_registry.render_agent_prompt(view, arguments.get("task", ""))}


LOCAL_HANDLERS = {
    "maestro-context": handle_maestro_context,
    "maestro-agent": handle_maestro_agent,
    "cv-status": cv_pipeline.cv_status,
    "cv-generate": cv_pipeline.cv_generate,
}


def get_tools() -> list[Tool]:
    """Get all available MCP tools"""
    agent_names = sorted(agent_registry.load_agents())
    return [
        Tool(
            name="maestro-context",
            description=(
                "[START HERE] Call once at the start of every session in mi-portafolio. Returns the session protocol, "
                "all .github/agents with their workflows/skills/MCP tools, key repo paths (CV pipeline) and "
                "agent<->maestro consistency issues."
            ),
            inputSchema={"type": "object", "properties": {}},
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
                "[CV] Check the CV pipeline: is cv/input/cv-data.json in sync with the generated web data, "
                "which files exist in cv/output and whether web downloads are synced"
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="cv-generate",
            description=(
                "[CV] Validate cv/input/cv-data.json (or another JSON with the same shape) and regenerate "
                "cv/output/*.pdf|docx plus packages/core/src/data/cv-data.generated.json"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Optional repo-relative JSON to use as the new cv/input/cv-data.json",
                    }
                },
            },
        ),
        Tool(
            name="maestro",
            description="[MAESTRO] Master orchestrator - Execute workflows: ci, test, deploy, portfolio-update, full-pipeline",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow": {
                        "type": "string",
                        "description": "Workflow to execute",
                        "enum": WORKFLOWS
                    },
                    "options": {
                        "type": "object",
                        "description": "Workflow options (verbose, dry_run, etc.)",
                        "default": {}
                    }
                },
                "required": ["workflow"]
            }
        ),
        Tool(
            name="maestro-plan",
            description="[PLAN] Preview maestro orchestration plan (specialized agents and skill sequence) without executing skills",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow": {
                        "type": "string",
                        "description": "Workflow to preview",
                        "enum": WORKFLOWS
                    }
                },
                "required": ["workflow"]
            }
        ),
        Tool(
            name="skill-type-checker",
            description="[CHECK] Run type checking (mypy for Python, tsc for TypeScript)",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-unit-test-runner",
            description="[TEST] Run unit tests (pytest for Python, vitest for TypeScript)",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-e2e-test-runner",
            description="[PLAY] Run E2E tests (Playwright)",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-build-orchestrator",
            description="[BUILD] Build all projects",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-quality-gate-runner",
            description="[GATE] Run quality gates",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-coverage-analyzer",
            description="[COVERAGE] Analyze and report test coverage",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-github-pages-deployer",
            description="[DEPLOY] Deploy artifacts to GitHub Pages",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-release-orchestrator",
            description="[RELEASE] Orchestrate release pipeline",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="skill-git-workflow-manager",
            description="[GIT] Execute git workflow operations",
            inputSchema={"type": "object", "properties": {}}
        ),
    ]


async def handle_list_tools(_ctx: Any, _params: PaginatedRequestParams) -> ListToolsResult:
    """Handle list tools request - MCP protocol method: tools/list"""
    logger.info("[TOOLS] Listing tools")
    tools = get_tools()
    logger.info(f"   Found {len(tools)} tools")
    return ListToolsResult(tools=tools)


async def handle_call_tool(_ctx: Any, params: CallToolRequestParams) -> CallToolResult:
    """Handle tool call request - MCP protocol method: tools/call"""
    tool_name = params.name
    arguments = params.arguments or {}
    
    logger.info(f"[CALL] Tool invoked: {tool_name}")
    logger.debug(f"   Arguments: {arguments}")
    
    try:
        if tool_name in LOCAL_HANDLERS:
            result = LOCAL_HANDLERS[tool_name](arguments)
            return CallToolResult(content=[TextContent(type="text", text=json.dumps(result, ensure_ascii=False))])

        handlers_mod = _load_handlers()
        
        # Map tool names to handler functions
        handler_map = {
            "maestro": "handle_maestro_async",
            "maestro-plan": "handle_maestro_plan_async",
            "skill-type-checker": "handle_type_checker_async",
            "skill-unit-test-runner": "handle_unit_test_runner_async",
            "skill-e2e-test-runner": "handle_e2e_test_runner_async",
            "skill-build-orchestrator": "handle_build_orchestrator_async",
            "skill-quality-gate-runner": "handle_quality_gate_runner_async",
            "skill-coverage-analyzer": "handle_coverage_analyzer_async",
            "skill-github-pages-deployer": "handle_github_pages_deployer_async",
            "skill-release-orchestrator": "handle_release_orchestrator_async",
            "skill-git-workflow-manager": "handle_git_workflow_manager_async",
        }
        
        handler_name = handler_map.get(tool_name)
        if not handler_name:
            error_msg = f"Tool '{tool_name}' not found"
            logger.warning(f"❌ {error_msg}")
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({"status": "error", "error": error_msg})
                )]
            )
        
        handler = getattr(handlers_mod, handler_name, None)
        if not handler:
            error_msg = f"Handler '{handler_name}' not implemented"
            logger.warning(f"❌ {error_msg}")
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({"status": "error", "error": error_msg})
                )]
            )
        
        # Execute handler
        if inspect.iscoroutinefunction(handler):
            result = await handler(arguments)
        else:
            result = handler(arguments)
        
        logger.info(f"✅ Tool completed: {tool_name}")
        
        # Ensure result is a string
        if isinstance(result, str):
            text_result = result
        else:
            text_result = json.dumps(result)
        
        return CallToolResult(
            content=[TextContent(type="text", text=text_result)]
        )
        
    except Exception as e:
        logger.error(f"❌ Tool error: {tool_name} - {str(e)}", exc_info=True)
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps({"status": "error", "error": str(e)})
            )]
        )


async def handle_list_prompts(_ctx: Any, _params: PaginatedRequestParams) -> ListPromptsResult:
    """Expose every .github/agents definition as an MCP prompt - MCP protocol method: prompts/list"""
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
    """Render an agent prompt with the MCP session protocol - MCP protocol method: prompts/get"""
    views, _ = _agent_views()
    view = views.get(params.name)
    if view is None:
        raise ValueError(f"Unknown agent prompt '{params.name}'")
    task = (params.arguments or {}).get("task", "")
    return GetPromptResult(
        description=view.spec.description,
        messages=[PromptMessage(role="user", content=TextContent(type="text", text=agent_registry.render_agent_prompt(view, task)))],
    )


async def main():
    """Main entry point - run MCP server over stdio"""
    logger.info("Starting Maestro MCP Server...")
    logger.info("Listening on stdio for MCP protocol messages")
    
    # MCP SDK 2.x: params_type must be a RequestParams model and handlers receive (ctx, params)
    server.add_request_handler("tools/list", PaginatedRequestParams, handle_list_tools)
    server.add_request_handler("tools/call", CallToolRequestParams, handle_call_tool)
    server.add_request_handler("prompts/list", PaginatedRequestParams, handle_list_prompts)
    server.add_request_handler("prompts/get", GetPromptRequestParams, handle_get_prompt)
    
    logger.info("Handlers registered")
    
    # Use stdio_server as the transport layer
    # stdio_server yields a tuple (read_stream, write_stream)
    async with stdio_server() as (read_stream, write_stream):
        logger.info("MCP Server is running and ready for protocol messages")
        # Run server with the stdio streams
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
