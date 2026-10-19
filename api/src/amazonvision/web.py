from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

_NOT_BUILT = """<!doctype html><html lang="pt-BR"><meta charset="utf-8">
<title>AmazonVision 4.0</title>
<body style="font-family:Segoe UI,sans-serif;padding:40px;color:#172C23;background:#F4F6F2">
<h1>Interface não compilada</h1>
<p>Rode <code>pnpm build</code> em <code>web/</code> ou use <code>scripts/dev.ps1</code>.</p>
</body></html>"""


def mount_web(app: FastAPI, dist: Path) -> None:
    """Serve the compiled SPA; unknown non-API paths fall back to index.html."""
    root = dist.resolve()

    @app.get("/{path:path}", include_in_schema=False)
    def spa(path: str):
        if path == "api" or path.startswith("api/"):
            raise HTTPException(status_code=404)
        index = root / "index.html"
        if not index.is_file():
            return HTMLResponse(_NOT_BUILT, status_code=503)
        candidate = (root / path).resolve()
        if path and candidate.is_file() and candidate.is_relative_to(root):
            return FileResponse(candidate)
        return FileResponse(index, headers={"Cache-Control": "no-cache"})
