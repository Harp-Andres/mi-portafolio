"""
Git, pull request and release skills.

GitHub Pages is only deployed by .github/workflows/deploy.yml on push to main, so these skills
verify and report; they never push.
"""

import repo_commands as cmd
from base_skill import CommandSkill


class GitHubPagesDeployer(CommandSkill):
    NAME = "github_pages_deployer"
    DESCRIPTION = "[DEPLOY] Build the site the Pages workflow deploys and report the latest deploy run on main"
    STEPS = (cmd.WEB_BUILD, cmd.LATEST_MAIN_DEPLOY)


class GitWorkflowManager(CommandSkill):
    NAME = "git_workflow_manager"
    DESCRIPTION = "[GIT] Current branch, pending changes and the pull requests of this branch (git status + gh pr status)"
    STEPS = (cmd.BRANCH_STATUS, cmd.PULL_REQUESTS)


class ReleaseOrchestrator(CommandSkill):
    NAME = "release_orchestrator"
    DESCRIPTION = "[RELEASE] Every CI check locally before merging to main: type-check, unit, backend, CV sync, E2E, build"
    STEPS = (
        cmd.WEB_TYPECHECK,
        cmd.WEB_UNIT_TESTS,
        cmd.BACKEND_TESTS,
        cmd.CV_WEB_SYNC,
        cmd.WEB_E2E,
        cmd.WEB_BUILD,
    )
