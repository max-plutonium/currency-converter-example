from datetime import timedelta
from typing import Optional, List

from dependency_injector import containers, providers
from fastapi import FastAPI

from app.services.apilayer.services import ApiLayerConverterService
from app.util import parse_timeout, get_app_version
from app.settings import Settings


def _create_server(title: str, debug: bool, version: str,
                   api_root: str, cors: Optional[List[str]] = None) -> FastAPI:
    from fastapi.responses import UJSONResponse
    from starlette.authentication import AuthenticationBackend, AuthCredentials, UnauthenticatedUser
    from starlette.middleware import Middleware
    from starlette.middleware.authentication import AuthenticationMiddleware
    from fastapi.middleware.cors import CORSMiddleware

    class AuthBackend(AuthenticationBackend):
        async def authenticate(self, request):
            return AuthCredentials(), UnauthenticatedUser()

    middlewares = [
        Middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in cors] if cors else ['*'],
            allow_credentials=True, allow_methods=['*'], allow_headers=['*'],
        ),
        Middleware(AuthenticationMiddleware, backend=AuthBackend()),
    ]

    server = FastAPI(
        title=title, version=version, debug=debug,
        default_response_class=UJSONResponse, root_path=api_root,
        middleware=middlewares
    )

    return server


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Factory(Settings)

    converter_service = providers.Selector(
        config.converter_type,
        apilayer=providers.Singleton(
            ApiLayerConverterService,
            config.apilayer.api_key,
            parse_timeout(config.apilayer.connection_timeout())
        ),
    )

    server = providers.Singleton(
        _create_server, settings.provided.PROJECT_SLUG,
        settings.provided.DEBUG, get_app_version(),
        settings.provided.API_ROOT, settings.provided.BACKEND_CORS_ORIGINS
    )
