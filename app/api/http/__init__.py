from typing import Any, Dict

from fastapi import Request, status, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import UJSONResponse


def init_http_api(app: FastAPI):
    from .converter import router as conv_router

    app.include_router(conv_router, prefix='/api')
    app.state.container.wire(packages=[__name__])

    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(_: Request, exc: RequestValidationError):
        error_dict = {}
        for e in exc.errors():  # type: Dict[str, Any]
            location = '.'.join([str(l) for l in e['loc'] if l != 'body'])
            if location in error_dict:
                error_dict[location] = [error_dict[location], {'msg': e['msg'], 'type': e['type']}]
            else:
                error_dict[location] = {'msg': e['msg'], 'type': e['type']}

        return UJSONResponse(error_dict, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @app.exception_handler(Exception)
    def exception_handler(_: Request, exc: Exception):
        error_dict = dict()
        error_dict['detail'] = f'{exc}'
        return UJSONResponse(error_dict, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
