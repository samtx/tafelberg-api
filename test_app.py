import pytest
from httpx import AsyncClient

from app import app

@pytest.mark.asyncio
async def test_home():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "Tafelberg API" in response.text


@pytest.mark.asyncio
async def test_properties():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get("/properties")
    assert response.status_code == 200
    properties = response.json()['properties']
    assert len(properties) == 4
