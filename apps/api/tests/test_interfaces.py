from __future__ import annotations

import json

import pytest

from app.interfaces.cli import main


def test_cli_status_json(backend, capsys):
    assert main(["status", "--json"], backend) == 0
    payload = json.loads(capsys.readouterr().out)
    assert set(payload) == {"inSync", "fingerprint", "jsonInSync", "documents", "pendingRequests"}
    assert len(payload["documents"]) == 4


def test_cli_apply_without_pending_requests_fails_cleanly(backend, capsys):
    assert main(["apply"], backend) == 1
    assert "No requests to apply" in capsys.readouterr().out


def test_cli_apply_processes_the_inbox_and_reports_domain_errors(backend, write_request, capsys):
    write_request("## Habilidades\n- categoria: Performance\n- agregar: k6\n")
    assert main(["apply"], backend) == 0
    assert "Skills added to 'Performance': k6" in capsys.readouterr().out

    write_request("## Eliminar\n- titulo: does not exist\n", name="bad.md")
    assert main(["apply"], backend) == 1
    assert "❌" in capsys.readouterr().out


def test_http_adapter_uses_the_same_use_cases(backend):
    testclient = pytest.importorskip("fastapi.testclient")
    from app.interfaces.http import create_app

    client = testclient.TestClient(create_app(backend))
    assert client.get("/health").json() == {"status": "ok"}

    response = client.post(
        "/api/cv/requests",
        json={"filename": "idioma.md", "content": "## Idioma\n- idioma: Francés\n- nivel: A1\n"},
    )
    assert response.status_code == 200, response.text
    assert response.json()["applied"] == ["Language set: Francés (A1)"]
    assert client.get("/api/cv/status").json()["inSync"] is True

    rejected = client.post("/api/cv/requests", json={"filename": "x.md", "content": "## Vacaciones\n- dias: 3\n"})
    assert rejected.status_code == 422
    assert client.get("/api/cv/documents/..%2Fcv-data.json").status_code == 404
