from decimal import Decimal

from dependency_injector.wiring import inject, Provide
from fastapi import Query, Depends
from fastapi.routing import APIRouter

from app.schemas.converter import ConvertResult
from app.services.converter import ConverterService
from app.containers import ApplicationContainer

router = APIRouter()


# noinspection PyIncorrectDocstring
@router.get('/rates', response_model=ConvertResult,
            description='Converts a value from one currency to another')
@inject
async def get_rates(
        from_: str = Query(..., alias='from'),
        to: str = Query(...),
        value: Decimal = Query(...),
        converter_service: ConverterService = Depends(Provide[ApplicationContainer.converter_service]),
):
    """
    Converts an amount from one currency to another
    :param from: Three-letter code of source currency
    :param to: Three-letter code of destination currency
    :param value: Value to convert
    :return: Convertion result
    """
    return await converter_service.convert(from_=from_, dest=to, value=value)
