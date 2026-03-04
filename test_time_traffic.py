import pytest
from unittest.mock import AsyncMock
import asyncio
from lab1 import time



@pytest.mark.asyncio
async def test_normal_traffic():

    mock_maps = AsyncMock()
    mock_maps.get_traffic_score.return_value = 5

    result = await time(100, 50, "трасса", mock_maps)

    assert result == 3.0
    mock_maps.get_traffic_score.assert_called_once_with("default")


@pytest.mark.asyncio
async def test_max_traffic():
    mock_maps = AsyncMock()
    mock_maps.get_traffic_score.return_value = 10

    result = await time(100, 50, "трасса", mock_maps)

    assert result == 4.0
    mock_maps.get_traffic_score.assert_called_once()


@pytest.mark.asyncio
async def test_no_traffic():
    mock_maps = AsyncMock()
    mock_maps.get_traffic_score.return_value = 0

    result = await time(100, 50, "трасса", mock_maps)

    assert result == 2.0


@pytest.mark.asyncio
async def test_city_with_traffic():

    mock_maps = AsyncMock()
    mock_maps.get_traffic_score.return_value = 5

    result = await time(60, 30, "город", mock_maps)

    assert result == 3.6


@pytest.mark.asyncio
async def test_traffic_service_unavailable():

    mock_maps = AsyncMock()
    mock_maps.get_traffic_score.side_effect = ConnectionError("API недоступен")

    result = await time(100, 50, "трасса", mock_maps)

    assert result == 2.0


@pytest.mark.asyncio
async def test_validation_from_lab1():
    mock_maps = AsyncMock()

    with pytest.raises(ValueError, match="Скорость не может превышать 150 км/ч"):
        await time(100, 200, "трасса", mock_maps)

    with pytest.raises(ValueError, match="В городе скорость не может превышать 60 км/ч"):
        await time(100, 70, "город", mock_maps)


@pytest.mark.asyncio
async def test_different_route_ids():
    mock_maps = AsyncMock()
    mock_maps.get_traffic_score.return_value = 3

    await time(100, 50, "трасса", mock_maps, route_id="route-123")

    mock_maps.get_traffic_score.assert_called_once_with("route-123")