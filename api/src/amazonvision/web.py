from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, Response

_NOT_BUILT = """<!doctype html><html lang="pt-BR"><meta charset="utf-8">
<title>AmazonVision 4.0</title>
<body style="font-family:Segoe UI,sans-serif;padding:40px;color:#172C23;background:#F4F6F2">
<h1>Interface não compilada</h1>
<p>Rode <code>pnpm build</code> em <code>web/</code> ou use <code>scripts/dev.ps1</code>.</p>
</body></html>"""


class SpaFiles:
    """Serves the compiled SPA as the fallback for unmatched non-API GET requests."""

    def __init__(self, dist: Path) -> None:
        self.root = dist.resolve()

    def response_for(self, path: str) -> Response:
        index = self.root / "index.html"
        if not index.is_file():
            return HTMLResponse(_NOT_BUILT, status_code=503)
        relative = path.lstrip("/")
        candidate = (self.root / relative).resolve()
        if relative and candidate.is_file() and candidate.is_relative_to(self.root):
            return FileResponse(candidate)
        return FileResponse(index, headers={"Cache-Control": "no-cache"})


def is_api_path(path: str) -> bool:
    return path == "/api" or path.startswith("/api/")


def mount_web(app: FastAPI, dist: Path) -> None:
    app.state.spa = SpaFiles(dist)
