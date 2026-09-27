"""
Agent registry - bridges `.github/agents/*.agent.md` with the maestro MCP server.

Agents -> MCP: every agent declares `maestro/*` in its `tools` frontmatter and
starts each session by calling `maestro-context`.
MCP -> agents: the server reads the agent definitions from disk, exposes each one
as an MCP prompt and reports which skills/workflows/tools belong to each agent.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = REPO_ROOT / ".github" / "agents"
MASTER_AGENT = "agent-master-portfolio"
MAESTRO_TOOLSET = "maestro/*"

SESSION_PROTOCOL: List[str] = [
    "1. Call `maestro-context` once at the start of the session (this payload).",
    "2. Pick the workflow that matches the task and call `maestro-plan` to get the agent -> skill sequence.",
    "3. Load the owning agent instructions with `maestro-agent` (or the MCP prompt of the same name) and act as that agent.",
    "4. Run the `skill-*` tools listed for that agent; verify any failed or suspiciously fast result with the native command and report it.",
    "5. Finish with lint + unit tests (`skill-type-checker`, `skill-unit-test-runner`) before proposing a commit/PR.",
]

KEY_PATHS: Dict[str, str] = {
    "cv_requests": "cv/input/requests/ (.md/.txt change requests; applied ones go to cv/input/processed/)",
    "cv_request_template": "cv/input/request-template.md",
    "cv_backend": "apps/api (python -m app status|apply|generate)",
    "cv_output": "cv/output/ (Word/PDF + cv-data.json, all stamped with the same fingerprint)",
    "cv_web_data": "cv/output/cv-data.json (read by packages/core)",
    "cv_web_downloads": "apps/web/public/cv/ (synced from cv/output on dev/build)",
    "certificates": "apps/web/public/certificados/",
    "agents": ".github/agents/",
    "instructions": ".github/instructions/",
    "prompts": ".github/prompts/",
    "cv_workflow_doc": "docs/CV_MANAGEMENT/WORKFLOW.md",
}

AGENT_EXTRA_TOOLS: Dict[str, List[str]] = {
    "portfolio-cv-manager": ["cv-status", "cv-apply", "cv-generate"],
}

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)


@dataclass(frozen=True)
class AgentSpec:
    name: str
    description: str
    tools: List[str]
    delegates: List[str]
    argument_hint: str
    instructions: str
    path: str


@dataclass
class AgentView:
    spec: AgentSpec
    skills: List[str] = field(default_factory=list)
    workflows: List[str] = field(default_factory=list)
    mcp_tools: List[str] = field(default_factory=list)

    def summary(self) -> Dict[str, Any]:
        return {
            "name": self.spec.name,
            "description": self.spec.description,
            "workflows": self.workflows,
            "skills": self.skills,
            "mcp_tools": self.mcp_tools,
            "delegates": self.spec.delegates,
            "path": self.spec.path,
        }

    def detail(self) -> Dict[str, Any]:
        return {**self.summary(), "argument_hint": self.spec.argument_hint, "instructions": self.spec.instructions}


def _parse_value(raw: str) -> Any:
    value = raw.strip()
    if value.startswith("[") and value.endswith("]"):
        return [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
    return value.strip("'\"")


def parse_agent_file(path: Path) -> AgentSpec:
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(text)
    meta: Dict[str, Any] = {}
    body = text
    if match:
        for line in match.group(1).splitlines():
            if ":" in line and not line.startswith((" ", "\t")):
                key, raw = line.split(":", 1)
                meta[key.strip()] = _parse_value(raw)
        body = match.group(2)
    return AgentSpec(
        name=path.name.removesuffix(".agent.md"),
        description=str(meta.get("description", "")),
        tools=list(meta.get("tools") or []),
        delegates=list(meta.get("agents") or []),
        argument_hint=str(meta.get("argument-hint", "")),
        instructions=body.strip(),
        path=path.relative_to(REPO_ROOT).as_posix(),
    )


def load_agents(agents_dir: Path = AGENTS_DIR) -> Dict[str, AgentSpec]:
    return {spec.name: spec for spec in (parse_agent_file(p) for p in sorted(agents_dir.glob("*.agent.md")))}


def skill_tool_name(skill: str) -> str:
    return "skill-" + skill.replace("_", "-")


def build_views(
    agents: Mapping[str, AgentSpec],
    skill_owner: Mapping[str, str],
    workflow_agents: Mapping[str, Sequence[str]],
    exposed_tools: Sequence[str],
) -> Dict[str, AgentView]:
    views = {name: AgentView(spec=spec) for name, spec in agents.items()}
    exposed = set(exposed_tools)
    for skill, owner in skill_owner.items():
        view = views.get(owner)
        if view is None:
            continue
        view.skills.append(skill)
        tool = skill_tool_name(skill)
        if tool in exposed:
            view.mcp_tools.append(tool)
    for name, tools in AGENT_EXTRA_TOOLS.items():
        if name in views:
            views[name].mcp_tools = [t for t in tools if t in exposed] + views[name].mcp_tools
    for workflow, members in workflow_agents.items():
        for member in members:
            if member in views:
                views[member].workflows.append(workflow)
    if MASTER_AGENT in views:
        master = views[MASTER_AGENT]
        master.workflows = list(workflow_agents)
        master.mcp_tools = sorted(exposed)
    return views


def consistency_issues(
    agents: Mapping[str, AgentSpec],
    skill_owner: Mapping[str, str],
    workflow_agents: Mapping[str, Sequence[str]],
) -> List[str]:
    issues: List[str] = []
    referenced = set(skill_owner.values()) | {a for members in workflow_agents.values() for a in members}
    for name in sorted(referenced - set(agents)):
        issues.append(f"maestro references agent '{name}' but .github/agents/{name}.agent.md does not exist")
    for name, spec in sorted(agents.items()):
        if MAESTRO_TOOLSET not in spec.tools:
            issues.append(f"agent '{name}' does not declare '{MAESTRO_TOOLSET}' in its tools frontmatter")
    master = agents.get(MASTER_AGENT)
    if master:
        for name in sorted(set(agents) - {MASTER_AGENT} - set(master.delegates)):
            issues.append(f"agent '{name}' is not listed in {MASTER_AGENT} 'agents' frontmatter")
    return issues


def build_context(
    views: Mapping[str, AgentView],
    workflow_agents: Mapping[str, Sequence[str]],
    issues: Sequence[str],
) -> Dict[str, Any]:
    return {
        "status": "success",
        "repo": "Harp-Andres/mi-portafolio",
        "protocol": SESSION_PROTOCOL,
        "workflows": {name: list(members) for name, members in workflow_agents.items()},
        "agents": [view.summary() for view in views.values()],
        "paths": KEY_PATHS,
        "consistency_issues": list(issues),
    }


def render_agent_prompt(view: AgentView, task: str = "") -> str:
    spec = view.spec
    lines = [
        f"Act as the `{spec.name}` agent of the mi-portafolio repo ({spec.path}).",
        "",
        "MCP session protocol:",
        *SESSION_PROTOCOL,
        "",
        f"Workflows: {', '.join(view.workflows) or 'none'}",
        f"Maestro tools for this agent: {', '.join(view.mcp_tools) or 'maestro-plan only'}",
        "",
        "Agent instructions:",
        spec.instructions,
    ]
    if task:
        lines += ["", f"Task: {task}"]
    return "\n".join(lines)
