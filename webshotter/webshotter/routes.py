import pathlib

from aiohttp import web

from webshotter.main.views import index, handle, screenshots

PROJECT_PATH = pathlib.Path(__file__).parent


def init_routes(app: web.Application) -> None:
    add_route = app.router.add_route

    # add_route('*', '/', index, name='index')
    add_route("POST", "/", handle)
    add_route("GET", "/", screenshots)

    # added static dir
    # app.router.add_static(
    #     '/static/',
    #     path=(PROJECT_PATH / 'static'),
    #     name='static',
    # )
