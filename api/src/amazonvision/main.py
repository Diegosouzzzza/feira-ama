import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

from amazonvision import __version__
from amazonvision.config import Settings
from amazonvision.core.logs import setup_logging
from amazonvision.http_errors import ERROR_RESPONSES, install_error_handlers
from amazonvision.openapi import install_openapi
from amazonvision.routes import (
    agreement,
    camera,
    control,
    dataset,
    diagnostics,
    exports,
    health,
    housekeeping,
    inspections,
    lots,
    machine,
    models,
    status,
    ws,
)
from amazonvision.services.container import Services
from amazonvision.web import mount_web

log = logging.getLogger("amazonvision")


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        settings.ensure_data_dirs()
        if settings.log_to_file:
            setup_logging(settings.data_subdirs["logs"])
        services = Services.create(settings)
        await services.start()
        app.state.services = services
        log.info("AmazonVision %s iniciado em modo %s", __version__, settings.mode)
        try:
            yield
        finally:
            await services.stop()
            log.info("AmazonVision encerrado")

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
    # Rejects requests whose Host is not local (protects against DNS rebinding).
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)
    install_error_handlers(app)
    for router in (
        health.router,
        status.router,
        control.router,
        lots.router,
        machine.router,
        models.router,
        inspections.router,
        diagnostics.router,
        camera.router,
        dataset.router,
        agreement.router,
        exports.router,
        housekeeping.router,
    ):
        app.include_router(router, prefix="/api", responses=ERROR_RESPONSES)
    app.include_router(ws.router, prefix="/api")
    mount_web(app, settings.web_dist)
    install_openapi(app)
    return app
