import aiohttp_cors  # type: ignore
from aiohttp.web import Application, get

from . import handlers as grab_handlers
from .containers import Container


def create_app() -> Application:
    container = Container()
    container.wire(modules=[grab_handlers])

    app = Application()

    app.container = container

    cors_default = {
        "http://localhost:8080": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        ),
        "http://0.0.0.0:8080": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        ),
        "http://api:8080": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        ),
    }

    cors = aiohttp_cors.setup(app, defaults=cors_default)

    app.add_routes([get("/hh", grab_handlers.grab)])

    for route in list(app.router.routes()):
        cors.add(route)

    return app
