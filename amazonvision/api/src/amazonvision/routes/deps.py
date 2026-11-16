from typing import Annotated

from fastapi import Depends, Header

from amazonvision.core.control import Grant
from amazonvision.services.container import Services, services_dep

ServicesDep = Annotated[Services, Depends(services_dep)]
ControlTokenHeader = Annotated[
    str | None, Header(alias="X-Control-Token", description="Token de controle do operador")
]


def require_control(services: ServicesDep, token: ControlTokenHeader = None) -> Grant:
    return services.control.verify(token)


ControlDep = Annotated[Grant, Depends(require_control)]
