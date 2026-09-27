"""Local HTTP adapter over the same use cases as the CLI (optional extra: `api`).

    uv run --project apps/api --extra api python apps/api/run.py
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.composition import CurriculumBackend, build_backend
from app.domain.errors import CurriculumError
from app.interfaces.presenters import documents_payload, status_payload


class ChangeRequestBody(BaseModel):
    filename: str = Field(pattern=r"^[\w.\- ]+\.(md|txt)$")
    content: str = Field(min_length=1)


def create_app(backend: CurriculumBackend) -> FastAPI:
    api = FastAPI(title="mi-portafolio CV backend", version="3.0.0")

    @api.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @api.get("/api/cv/status")
    def status() -> dict:
        return status_payload(backend.status.execute())

    @api.post("/api/cv/requests")
    def apply_request(body: ChangeRequestBody) -> dict:
        request = backend.paths.requests_dir / body.filename
        request.parent.mkdir(parents=True, exist_ok=True)
        request.write_text(body.content, encoding="utf-8")
        try:
            result = backend.apply_request.execute(request)
        except CurriculumError as error:
            request.unlink(missing_ok=True)
            raise HTTPException(status_code=422, detail=str(error)) from None
        return {"applied": result.applied, "documents": documents_payload(result.generation.documents)}

    @api.post("/api/cv/generate")
    def generate() -> dict:
        try:
            return {"documents": documents_payload(backend.generate.execute().documents)}
        except CurriculumError as error:
            raise HTTPException(status_code=422, detail=str(error)) from None

    @api.get("/api/cv/documents/{filename}")
    def document(filename: str) -> FileResponse:
        path = backend.paths.output_dir / filename
        if path.parent != backend.paths.output_dir or not path.is_file():
            raise HTTPException(status_code=404, detail="Document not found")
        return FileResponse(path, filename=filename)

    return api


app = create_app(build_backend())
