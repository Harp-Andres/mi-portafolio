"""Run the local HTTP adapter: uv run --project apps/api --extra api python apps/api/run.py"""

import sys
from pathlib import Path

import uvicorn

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    uvicorn.run("app.interfaces.http:app", host="127.0.0.1", port=8000, reload=False)
