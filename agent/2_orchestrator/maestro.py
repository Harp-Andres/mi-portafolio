"""Maestro orchestrator: turns a workflow into an agent -> skill plan and runs its skills in order."""

from typing import Any, Dict, List

import skill_registry
from base_skill import SkillRequest
from workflows import SKILL_OWNER, WORKFLOW_AGENTS, WORKFLOW_SKILLS

MASTER_AGENT = "agent-master-portfolio"


def owner_of(skill: str) -> str:
    return SKILL_OWNER.get(skill, MASTER_AGENT)


def build_plan(workflow: str) -> List[Dict[str, Any]]:
    """Group the workflow skills by owning agent, in the workflow's agent order."""
    by_agent: Dict[str, List[str]] = {}
    for skill in WORKFLOW_SKILLS.get(workflow, []):
        by_agent.setdefault(owner_of(skill), []).append(skill)
    plan = [{"agent": agent, "skills": by_agent.pop(agent)} for agent in WORKFLOW_AGENTS.get(workflow, []) if agent in by_agent]
    return plan + [{"agent": agent, "skills": skills} for agent, skills in by_agent.items()]


def describe(workflow: str) -> Dict[str, Any]:
    if workflow not in WORKFLOW_SKILLS:
        return {"status": "failed", "error": f"Unknown workflow: {workflow}", "workflow": workflow, "orchestration_plan": []}
    return {
        "status": "success",
        "workflow": workflow,
        "workflow_skills": WORKFLOW_SKILLS[workflow],
        "orchestration_plan": build_plan(workflow),
    }


def run_skill(name: str, verbose: bool = False) -> Dict[str, Any]:
    result = skill_registry.create_skill(name).execute(SkillRequest(verbose=verbose))
    return {"skill": name, "agent": owner_of(name), **result.to_dict()}


def run_workflow(workflow: str, continue_on_error: bool = False, verbose: bool = False) -> Dict[str, Any]:
    report = describe(workflow)
    if report["status"] != "success":
        return report
    skills = WORKFLOW_SKILLS[workflow]
    stages: List[Dict[str, Any]] = []
    for name in skills:
        stages.append(run_skill(name, verbose))
        if not stages[-1]["success"] and not continue_on_error:
            break
    passed = len(stages) == len(skills) and all(stage["success"] for stage in stages)
    return {**report, "status": "success" if passed else "failed", "stages": stages}
