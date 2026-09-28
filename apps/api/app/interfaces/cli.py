"""Command line entry point used by pnpm scripts, the MCP server and the agents.

    python -m app status [--json]
    python -m app apply [request.md ...]     # no paths = every pending file in cv/input/requests
    python -m app generate
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from app.composition import CurriculumBackend, build_backend
from app.domain.errors import CurriculumError
from app.interfaces.presenters import repo_relative as _rel
from app.interfaces.presenters import status_payload


def cmd_status(backend: CurriculumBackend, args: argparse.Namespace) -> int:
    report = backend.status.execute()
    if args.json:
        print(json.dumps(status_payload(report), ensure_ascii=False, indent=2))
        return 0
    print(f"CV fingerprint: {report.fingerprint[:12]}")
    print(f"{'✅' if report.json_in_sync else '⚠️'} {_rel(backend.paths.state_file)}")
    for doc in report.documents:
        mark = "✅" if doc.in_sync else ("⚠️" if doc.exists else "❌")
        print(f"{mark} cv/output/{doc.name}")
    for request in report.pending_requests:
        print(f"📝 pending request: {_rel(request)}")
    if not report.in_sync:
        print("Run `pnpm cv:generate` to re-render the documents.")
    return 0


def cmd_apply(backend: CurriculumBackend, args: argparse.Namespace) -> int:
    requests = [Path(p).resolve() for p in args.requests] or backend.status.execute().pending_requests
    if not requests:
        print(f"No requests to apply. Add a .md/.txt file to {_rel(backend.paths.requests_dir)}.")
        return 1
    for request in requests:
        result = backend.apply_request.execute(request)
        print(f"📝 {_rel(request)}")
        for line in result.applied:
            print(f"   ✅ {line}")
        print(f"   📦 archived as {_rel(result.archived_request)}")
    _print_documents(backend, result.generation.documents)
    return 0


def cmd_generate(backend: CurriculumBackend, args: argparse.Namespace) -> int:
    _print_documents(backend, backend.generate.execute().documents)
    return 0


def _print_documents(backend: CurriculumBackend, documents) -> None:
    for document in documents:
        print(f"✅ {_rel(document.path)}")
    print(f"✅ {_rel(backend.paths.state_file)}")
    print("🎉 CV documents and web data updated. The web picks them up on the next `pnpm dev` / `pnpm build`.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m app", description="mi-portafolio CV backend")
    commands = parser.add_subparsers(dest="command", required=True)

    status = commands.add_parser("status", help="Are Word/PDF and web data in sync? Pending requests?")
    status.add_argument("--json", action="store_true", help="machine-readable output")
    status.set_defaults(handler=cmd_status)

    apply = commands.add_parser("apply", help="Apply .md/.txt change requests and regenerate everything")
    apply.add_argument("requests", nargs="*", help="request files (default: pending files in cv/input/requests)")
    apply.set_defaults(handler=cmd_apply)

    generate = commands.add_parser("generate", help="Re-render Word/PDF and web data from the current CV")
    generate.set_defaults(handler=cmd_generate)
    return parser


def main(argv: list[str] | None = None, backend: CurriculumBackend | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = build_parser().parse_args(argv)
    try:
        return args.handler(backend or build_backend(), args)
    except CurriculumError as error:
        print(f"❌ {error}")
        return 1
