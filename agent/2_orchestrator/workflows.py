"""
Workflow catalog: which skills each workflow runs, which agent owns each skill and the order in
which agents take part. Keep agent names in sync with .github/agents (guarded by agent/tests).
"""

from typing import Dict, List

WORKFLOW_SKILLS: Dict[str, List[str]] = {
    "ci": ["dependency_resolver", "type_checker", "unit_test_runner", "build_orchestrator"],
    "test": ["unit_test_runner", "e2e_test_runner", "coverage_analyzer"],
    "deploy": ["quality_gate_runner", "github_pages_deployer"],
    "portfolio-update": ["cv_sync_checker", "unit_test_runner"],
    "quality": ["type_checker", "coverage_analyzer", "quality_gate_runner"],
    "full-pipeline": [
        "dependency_resolver",
        "quality_gate_runner",
        "e2e_test_runner",
        "cv_sync_checker",
        "git_workflow_manager",
        "github_pages_deployer",
    ],
}

SKILL_OWNER: Dict[str, str] = {
    "dependency_resolver": "devops-cicd-manager",
    "type_checker": "software-architecture-manager",
    "build_orchestrator": "devops-cicd-manager",
    "quality_gate_runner": "devops-cicd-manager",
    "unit_test_runner": "sdet-quality-manager",
    "e2e_test_runner": "portfolio-test-manager",
    "coverage_analyzer": "sdet-quality-manager",
    "github_pages_deployer": "portfolio-deployment-manager",
    "git_workflow_manager": "github-cicd-manager",
    "release_orchestrator": "github-cicd-manager",
    "cv_sync_checker": "portfolio-cv-manager",
}

WORKFLOW_AGENTS: Dict[str, List[str]] = {
    "ci": [
        "setup-portability-manager",
        "devops-cicd-manager",
        "software-architecture-manager",
        "sdet-quality-manager",
    ],
    "test": [
        "setup-portability-manager",
        "sdet-quality-manager",
        "portfolio-test-manager",
    ],
    "deploy": [
        "devops-cicd-manager",
        "platform-architecture-manager",
        "github-cicd-manager",
        "portfolio-deployment-manager",
    ],
    "portfolio-update": [
        "software-architecture-manager",
        "portfolio-cv-manager",
        "portfolio-test-manager",
    ],
    "quality": [
        "software-architecture-manager",
        "sdet-quality-manager",
        "devops-cicd-manager",
    ],
    "full-pipeline": [
        "setup-portability-manager",
        "devops-cicd-manager",
        "software-architecture-manager",
        "sdet-quality-manager",
        "portfolio-test-manager",
        "platform-architecture-manager",
        "github-cicd-manager",
        "portfolio-deployment-manager",
        "portfolio-cv-manager",
        "os-platform-manager",
    ],
}
