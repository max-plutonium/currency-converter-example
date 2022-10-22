from decimal import Decimal
from unittest import mock

import pytest
from dependency_injector import providers

from app.services.converter import ConverterService
from app.schemas.converter import ConvertResult
from app.config import app_container


@pytest.mark.asyncio
async def test_mocked(async_client):
    client_mock = mock.AsyncMock(spec=ConverterService)

    client_mock.convert.return_value = ConvertResult(
        success=True, result=Decimal(50)
    )

    with app_container.converter_service.override(providers.Object(client_mock)):
        response = await async_client.get(
            '/api/rates',
            params={
                'from': 'USD',
                'to': 'RUB',
                'value': 1,
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['result'] == 50
    assert data['error'] is None

    client_mock.convert.assert_called_once_with(
        from_='USD', dest='RUB', value=1
    )


@pytest.mark.asyncio
async def test_real(async_client):
    response = await async_client.get(
        '/api/rates',
        params={
            'from': 'USD',
            'to': 'RUB',
            'value': 1,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['result'] > 0
    assert data['error'] is None


@pytest.mark.asyncio
async def test_real_wrong_value(async_client):
    response = await async_client.get(
        '/api/rates',
        params={
            'from': 'USD',
            'to': 'RUB',
            'value': -1,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data['success'] is False
    assert data['result'] is None
    assert len(['error']) > 0
