"""Name -> class registry of every maestro skill."""

from pathlib import Path
from typing import Dict, Type

import cv_skills
import deployment_skills
import infrastructure_skills
import testing_skills
from base_skill import REPO_ROOT, BaseSkill

SKILLS: Dict[str, Type[BaseSkill]] = {
    skill.NAME: skill
    for skill in (
        infrastructure_skills.DependencyResolver,
        infrastructure_skills.TypeChecker,
        infrastructure_skills.BuildOrchestrator,
        infrastructure_skills.QualityGateRunner,
        testing_skills.UnitTestRunner,
        testing_skills.E2ETestRunner,
        testing_skills.CoverageAnalyzer,
        deployment_skills.GitHubPagesDeployer,
        deployment_skills.GitWorkflowManager,
        deployment_skills.ReleaseOrchestrator,
        cv_skills.CvSyncChecker,
    )
}


def create_skill(name: str, workspace_root: Path = REPO_ROOT) -> BaseSkill:
    skill = SKILLS.get(name)
    if skill is None:
        raise KeyError(f"Unknown skill '{name}'; registered: {sorted(SKILLS)}")
    return skill(workspace_root)
