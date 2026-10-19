import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from amazonvision import __version__
from amazonvision.config import Settings
from amazonvision.http_errors import ERROR_RESPONSES, install_error_handlers
from amazonvision.openapi import install_openapi
from amazonvision.routes import health
from amazonvision.web import mount_web

log = logging.getLogger("amazonvision")


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        settings.ensure_data_dirs()
        log.info("AmazonVision %s iniciado em modo %s", __version__, settings.mode)
        yield

    app = FastAPI(
        title="AmazonVision 4.0 API",
        version=__version__,
        description="Serviço local de inspeção visual e controle da bancada. Contrato: docs/api.md",
        lifespan=lifespan,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        redoc_url=None,
    )
    app.state.settings = settings
    install_error_handlers(app)
    app.include_router(health.router, prefix="/api", responses=ERROR_RESPONSES)
    mount_web(app, settings.web_dist)
    install_openapi(app)
    return app
