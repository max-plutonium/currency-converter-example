from app.config import app_container


server = app_container.server()
server.state.container = app_container


@server.on_event('startup')
def startup():
    from app.api.http import init_http_api

    init_http_api(server)
