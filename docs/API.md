# CV backend HTTP API (local, optional)

`apps/api` exposes the same use cases as the CLI (`pnpm cv:*`) over HTTP for local tooling.
The public web does **not** call it: GitHub Pages only serves the files in `cv/output/`.

```bash
pnpm dev:backend   # uv run --project apps/api --extra api python apps/api/run.py → http://127.0.0.1:8000
```

| Method | Path | Body | Result |
|--------|------|------|--------|
| `GET` | `/health` | — | `{"status": "ok"}` |
| `GET` | `/api/cv/status` | — | `inSync`, `fingerprint`, `documents[]`, `pendingRequests[]` |
| `POST` | `/api/cv/requests` | `{"filename": "x.md", "content": "## Curso\n- titulo: ..."}` | `applied[]`, `documents[]`; `422` with the problem if the request is rejected (nothing changes) |
| `POST` | `/api/cv/generate` | — | `documents[]` re-rendered from the current CV |
| `GET` | `/api/cv/documents/{file}` | — | Downloads a file from `cv/output/` |

The request format is documented in [CV_MANAGEMENT/WORKFLOW.md](./CV_MANAGEMENT/WORKFLOW.md#formato-de-la-solicitud).
Interactive docs: `http://127.0.0.1:8000/docs`.
