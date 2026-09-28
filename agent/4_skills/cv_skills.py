"""CV pipeline checks: the backend output and the web data must come from the same CV."""

import json

import repo_commands as cmd
from base_skill import CommandSkill, SkillFailed, SkillRequest


class CvSyncChecker(CommandSkill):
    NAME = "cv_sync_checker"
    DESCRIPTION = (
        "[CV] Fail if CV change requests are pending or cv/output (Word/PDF/cv-data.json) is out of sync, "
        "then check that the web reads the current CV"
    )
    STEPS = (cmd.CV_WEB_SYNC,)

    def _run(self, request: SkillRequest) -> str:
        result = self.run_command(cmd.CV_STATUS.command, cmd.CV_STATUS.timeout)
        if result.returncode != 0:
            raise SkillFailed(f"CV backend status failed:\n{result.stderr.strip()[-2000:]}")
        status = json.loads(result.stdout)
        if status["pendingRequests"]:
            raise SkillFailed(f"Pending CV requests (apply them with cv-apply): {status['pendingRequests']}")
        if not status["inSync"]:
            raise SkillFailed("cv/output is out of sync with the CV; run cv-generate")
        return "\n".join(["PASS CV backend status: in sync, no pending requests", self.run_steps(self.STEPS, request)])
