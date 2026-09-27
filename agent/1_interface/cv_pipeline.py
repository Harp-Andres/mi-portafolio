"""
CV pipeline tools for the maestro MCP server.

cv-status   -> is cv/input/cv-data.json in sync with the generated web data and cv/output?
cv-generate -> runs scripts/hv/generate-cv-pdf.py (validates input, writes cv/output + web JSON).
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Dict

from agent_registry import REPO_ROOT

INPUT_JSON = REPO_ROOT / "cv" / "input" / "cv-data.json"
OUTPUT_DIR = REPO_ROOT / "cv" / "output"
WEB_DATA_JSON = REPO_ROOT / "packages" / "core" / "src" / "data" / "cv-data.generated.json"
GENERATOR = REPO_ROOT / "scripts" / "hv" / "generate-cv-pdf.py"
PUBLIC_CV = REPO_ROOT / "apps" / "web" / "public" / "cv"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def cv_status(_arguments: Dict[str, Any]) -> Dict[str, Any]:
    if not INPUT_JSON.is_file():
        return {"status": "error", "error": f"Missing {INPUT_JSON.relative_to(REPO_ROOT).as_posix()}"}
    generated_digest = None
    if WEB_DATA_JSON.is_file():
        generated_digest = json.loads(WEB_DATA_JSON.read_text(encoding="utf-8")).get("_meta", {}).get("sourceSha256")
    in_sync = generated_digest == _digest(INPUT_JSON)
    outputs = sorted(p.name for p in OUTPUT_DIR.glob("*") if p.suffix in {".pdf", ".docx"}) if OUTPUT_DIR.is_dir() else []
    downloads = sorted(p.name for p in PUBLIC_CV.glob("*")) if PUBLIC_CV.is_dir() else []
    return {
        "status": "success",
        "input": "cv/input/cv-data.json",
        "generated_in_sync": in_sync,
        "cv_output": outputs,
        "web_downloads_synced": downloads == outputs,
        "next_step": "none" if in_sync else "call cv-generate (or `pnpm generate:cv`)",
    }


def cv_generate(arguments: Dict[str, Any]) -> Dict[str, Any]:
    command = ["uv", "run", str(GENERATOR)]
    input_path = arguments.get("input_path")
    if input_path:
        command.append(str((REPO_ROOT / input_path).resolve()))
    try:
        result = subprocess.run(
            command, cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=300
        )
    except FileNotFoundError:
        return {"status": "error", "error": "`uv` not found on PATH; install uv or run `pnpm generate:cv`"}
    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "CV generation timed out after 300 s"}
    return {
        "status": "success" if result.returncode == 0 else "failed",
        "exit_code": result.returncode,
        "output": result.stdout.strip(),
        "errors": result.stderr.strip()[-2000:],
        "next_step": "run `pnpm -F @mportafolio/web test` and review `git diff cv/`" if result.returncode == 0 else "fix the input problems listed in output",
    }
