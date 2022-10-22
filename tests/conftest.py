import asyncio

import httpx
import pytest
import pytest_asyncio

from fastapi.testclient import TestClient

from app.application import server


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def client(event_loop):
    with TestClient(server) as client:
        yield client


@pytest.mark.asyncio
@pytest_asyncio.fixture(scope='session')
async def async_client(client):
    async with httpx.AsyncClient(app=server, base_url=client.base_url) as aclient:
        yield aclient
