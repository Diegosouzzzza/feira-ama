from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel

from amazonvision import __version__
from amazonvision.config import RunMode, Settings

router = APIRouter(tags=["sistema"])


class HealthResponse(BaseModel):
    status: Literal["ok"]
    version: str
    mode: RunMode


@router.get("/health", response_model=HealthResponse)
def health(request: Request) -> HealthResponse:
    settings: Settings = request.app.state.settings
    return HealthResponse(status="ok", version=__version__, mode=settings.mode)
