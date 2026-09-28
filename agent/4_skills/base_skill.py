"""
Skill base classes.

A skill runs repo commands (pnpm, uv, git, gh) and reports a SkillResult. Most skills are a
`CommandSkill` that only declares its `STEPS`; the commands themselves live in repo_commands.py.
"""

from __future__ import annotations

import shutil
import subprocess
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_TAIL_CHARS = 4000


class SkillStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass(frozen=True)
class SkillRequest:
    verbose: bool = False


@dataclass(frozen=True)
class SkillResult:
    status: SkillStatus
    message: str
    duration_seconds: float
    output: str = ""
    errors: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    @property
    def success(self) -> bool:
        return self.status is SkillStatus.SUCCESS

    def to_dict(self) -> Dict[str, Any]:
        return {**asdict(self), "status": self.status.value, "success": self.success}


class SkillFailed(Exception):
    """A skill check did not pass; the message is reported to the caller."""


@dataclass(frozen=True)
class Step:
    label: str
    command: Tuple[str, ...]
    timeout: int = 600
    show_output: bool = False


def tail(text: str, limit: int = OUTPUT_TAIL_CHARS) -> str:
    text = text.strip()
    return text if len(text) <= limit else "..." + text[-limit:]


class BaseSkill(ABC):
    NAME: ClassVar[str]
    DESCRIPTION: ClassVar[str]

    def __init__(self, workspace_root: Path = REPO_ROOT) -> None:
        self.workspace_root = Path(workspace_root)

    def execute(self, request: SkillRequest = SkillRequest()) -> SkillResult:
        start = time.perf_counter()
        try:
            output = self._run(request)
        except subprocess.TimeoutExpired as exc:
            return self._result(SkillStatus.TIMEOUT, start, errors=[f"`{_join(exc.cmd)}` timed out after {exc.timeout}s"])
        except (SkillFailed, OSError) as exc:
            return self._result(SkillStatus.FAILED, start, errors=[str(exc)])
        return self._result(SkillStatus.SUCCESS, start, output=output)

    @abstractmethod
    def _run(self, request: SkillRequest) -> str:
        """Do the work and return a report; raise SkillFailed when a check does not pass."""

    def run_command(self, command: Sequence[str], timeout: int = 600) -> subprocess.CompletedProcess:
        # shutil.which resolves Windows shims such as pnpm.cmd, which subprocess cannot run by bare name.
        executable = shutil.which(command[0]) or command[0]
        return subprocess.run(
            [executable, *command[1:]],
            cwd=self.workspace_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )

    def _result(self, status: SkillStatus, start: float, output: str = "", errors: List[str] | None = None) -> SkillResult:
        verb = {SkillStatus.SUCCESS: "passed", SkillStatus.FAILED: "failed", SkillStatus.TIMEOUT: "timed out"}[status]
        return SkillResult(
            status=status,
            message=f"{self.NAME} {verb}",
            duration_seconds=round(time.perf_counter() - start, 2),
            output=output,
            errors=errors or [],
        )


class CommandSkill(BaseSkill):
    """Runs `STEPS` in order and stops at the first one that exits non-zero."""

    STEPS: ClassVar[Tuple[Step, ...]] = ()

    def _run(self, request: SkillRequest) -> str:
        return self.run_steps(self.STEPS, request)

    def run_steps(self, steps: Sequence[Step], request: SkillRequest) -> str:
        report: List[str] = []
        for step in steps:
            result = self.run_command(step.command, step.timeout)
            if result.returncode != 0:
                report.append(f"FAIL {step.label}: `{_join(step.command)}` exited with {result.returncode}")
                report.append(tail(result.stdout + "\n" + result.stderr))
                raise SkillFailed("\n".join(report))
            report.append(f"PASS {step.label}")
            if step.show_output or request.verbose:
                report.append(tail(result.stdout))
        return "\n".join(report)


def _join(command: Sequence[str] | str) -> str:
    return command if isinstance(command, str) else " ".join(str(part) for part in command)
