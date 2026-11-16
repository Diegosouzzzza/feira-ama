from typing import Any, Literal

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import TypeAdapter

from amazonvision.schemas import api as s
from amazonvision.schemas.errors import ApiErrorBody
from amazonvision.schemas.events import WsEvent

# Contract types published before their routes exist, so web/ can generate types now.
CONTRACT_INPUTS: dict[str, Any] = {
    "LotCreate": s.LotCreate,
    "MachineCommandRequest": s.MachineCommandRequest,
    "ControlClaim": s.ControlClaim,
    "InspectionReviewCreate": s.InspectionReviewCreate,
}
CONTRACT_OUTPUTS: dict[str, Any] = {
    "ApiErrorBody": ApiErrorBody,
    "SystemStatus": s.SystemStatus,
    "ProductOut": s.ProductOut,
    "ModelOut": s.ModelOut,
    "LotOut": s.LotOut,
    "LotSummary": s.LotSummary,
    "MachineCommandResult": s.MachineCommandResult,
    "ControlGrant": s.ControlGrant,
    "CycleOut": s.CycleOut,
    "InspectionOut": s.InspectionOut,
    "InspectionPage": s.InspectionPage,
    "ReviewOut": s.ReviewOut,
    "WsEvent": WsEvent,
}

_REF = "#/components/schemas/{model}"


def _merge(
    target: dict[str, Any], types: dict[str, Any], mode: Literal["validation", "serialization"]
) -> None:
    for name, tp in types.items():
        schema = TypeAdapter(tp).json_schema(ref_template=_REF, mode=mode)
        for def_name, definition in schema.pop("$defs", {}).items():
            target.setdefault(def_name, definition)
        target.setdefault(name, schema)


def install_openapi(app: FastAPI) -> None:
    def build() -> dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema
        schema = get_openapi(
            title=app.title, version=app.version, description=app.description, routes=app.routes
        )
        components = schema.setdefault("components", {}).setdefault("schemas", {})
        _merge(components, CONTRACT_INPUTS, "validation")
        _merge(components, CONTRACT_OUTPUTS, "serialization")
        app.openapi_schema = schema
        return schema

    app.openapi = build  # type: ignore[method-assign]
