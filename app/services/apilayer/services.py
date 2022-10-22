from datetime import timedelta
from decimal import Decimal
from typing import Optional

import httpx
import pydantic
from httpx import codes

from ..converter import ConverterService
from .schemas import ConvertResp

from app.schemas.converter import ConvertResult


class ApiLayerConverterService(ConverterService):
    base_url: str = 'https://api.apilayer.com/'

    def __init__(self, api_key: str, connection_timeout: Optional[timedelta] = None):
        self._api_key = api_key
        self._connection_timeout = connection_timeout

    @property
    def name(self) -> str:
        return 'ApiLayer'

    async def convert(self, from_: str, dest: str, value: Decimal) -> ConvertResult:
        from app import logger

        try:
            async with httpx.AsyncClient(base_url=self.base_url, timeout=self._connection_timeout.total_seconds()) as http:
                logger.debug(f'HTTP GET to "{http.base_url}/fixer/convert?from={from_}&to={dest}&amount={value}"')

                r = await http.get(
                    f'/fixer/convert?from={from_}&to={dest}&amount={value}',
                    params={'from': from_, 'to': dest, 'amount': value},
                    headers={'apikey': self._api_key}
                )

            if r.status_code != codes.OK:
                logger.error(f'Http error: {r.status_code}')
                return ConvertResult(success=False, error=f'Http error: {r.status_code}')

            resp = ConvertResp(**r.json())

        except httpx.HTTPError as e:
            logger.exception(f'Http error: {e}')
            return ConvertResult(success=False, error='Http error')
        except pydantic.ValidationError as e:
            logger.exception(f'Validation error: {e}')
            return ConvertResult(success=False, error=f'Validation error: "{e}"')
        except Exception as e:
            logger.exception(f'Unexpected error: {e}')
            return ConvertResult(success=False, error=f'Unexpected error: {e}')

        if not resp.success:
            logger.error(f'ApiLayer error: code={resp.error.code}, '
                         f'type="{resp.error.type_}", info={resp.error.info}')
            return ConvertResult(success=False, error=resp.error.info)

        return ConvertResult(success=True, result=resp.result)
