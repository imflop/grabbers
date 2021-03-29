from aiohttp.web import (
    Request,
    Response,
    json_response,
)
from dependency_injector.wiring import Provide, inject

from .containers import Container
from .services import HHService


@inject
async def grab(request: Request, hh_service: HHService = Provide[Container.hh_service]) -> Response:
    _ = request.query.get("query")
    data = await hh_service.search("Remote")

    return json_response(data)
