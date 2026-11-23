"""
CV tools of the maestro MCP server: a thin adapter over the CV backend CLI (apps/api).

The MCP never touches CV data itself; it forwards to `python -m app` so the agent, pnpm and
the HTTP adapter all run the same use cases.

cv-status   -> are the Word/PDF and the web JSON in sync? which requests are pending?
cv-apply    -> apply a change request (.md/.txt path, or the content written from chat)
cv-generate -> re-render Word/PDF + web JSON from the current CV
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List

from agent_registry import REPO_ROOT

BACKEND_PROJECT = REPO_ROOT / "apps" / "api"
_SAFE_NAME = re.compile(r"^[\w.\- ]+\.(md|txt)$")
_SAFE_VARIANT = re.compile(r"^[a-z0-9-]+$")
DEFAULT_CV_VARIANT = "qa"


def _variant(arguments: Dict[str, Any]) -> str:
    variant = str(arguments.get("variant") or DEFAULT_CV_VARIANT)
    if not _SAFE_VARIANT.fullmatch(variant):
        raise ValueError("variant must contain only lowercase letters, digits and hyphens")
    return variant


def _backend(variant: str, *args: str) -> subprocess.CompletedProcess | Dict[str, Any]:
    command = ["uv", "run", "--project", str(BACKEND_PROJECT), "python", "-m", "app", *args, "--variant", variant]
    try:
        return subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=300)
    except FileNotFoundError:
        return {"status": "error", "error": "`uv` not found on PATH; install uv or use the pnpm cv:* scripts"}
    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "The CV backend timed out after 300 s"}


def _report(result: subprocess.CompletedProcess | Dict[str, Any], next_step: str) -> Dict[str, Any]:
    if isinstance(result, dict):
        return result
    ok = result.returncode == 0
    return {
        "status": "success" if ok else "failed",
        "exit_code": result.returncode,
        "output": result.stdout.strip(),
        "errors": result.stderr.strip()[-2000:],
        "next_step": next_step if ok else "fix the problems listed in output and call the tool again",
    }


def cv_status(_arguments: Dict[str, Any]) -> Dict[str, Any]:
    try:
        result = _backend(_variant(_arguments), "status", "--json")
    except ValueError as error:
        return {"status": "error", "error": str(error)}
    if isinstance(result, dict):
        return result
    if result.returncode != 0:
        return _report(result, "")
    payload = json.loads(result.stdout)
    pending = payload["pendingRequests"]
    if pending:
        next_step = "call cv-apply to apply the pending requests"
    elif not payload["inSync"]:
        next_step = "call cv-generate"
    else:
        next_step = "none"
    return {"status": "success", **payload, "next_step": next_step}


def cv_apply(arguments: Dict[str, Any]) -> Dict[str, Any]:
    try:
        variant = _variant(arguments)
    except ValueError as error:
        return {"status": "error", "error": str(error)}
    args: List[str] = ["apply"]
    content = arguments.get("content")
    if content:
        filename = arguments.get("filename") or "chat-request.md"
        if not _SAFE_NAME.match(filename):
            return {"status": "error", "error": "filename must be a plain .md/.txt name"}
        request_dir = REPO_ROOT / "cv" / variant / "input" / "requests"
        request_dir.mkdir(parents=True, exist_ok=True)
        request = request_dir / filename
        request.write_text(content, encoding="utf-8")
        args.append(str(request))
    elif arguments.get("request_path"):
        args.append(str((REPO_ROOT / arguments["request_path"]).resolve()))
    return _report(_backend(variant, *args), "run `pnpm -F @mportafolio/web test` and review `git diff cv/`")


def cv_generate(_arguments: Dict[str, Any]) -> Dict[str, Any]:
    try:
        return _report(
            _backend(_variant(_arguments), "generate"),
            "run `pnpm -F @mportafolio/web test` and review `git diff cv/`",
        )
    except ValueError as error:
        return {"status": "error", "error": str(error)}
