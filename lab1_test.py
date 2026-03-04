import pytest
from lab1 import time


@pytest.mark.asyncio
async def test_1_high():
    result = await time(100, 50, "трасса")
    assert result == 2.0


@pytest.mark.asyncio
async def test_1_city():
    result = await time(60, 30, "город")
    assert result == 2.4


@pytest.mark.asyncio
async def test_negative():
    with pytest.raises(ValueError, match="Расстояние должно быть положительным"):
        await time(-100, 50, "трасса")


@pytest.mark.asyncio
async def test_zero_distance():
    with pytest.raises(ValueError, match="Расстояние должно быть положительным"):
        await time(0, 50, "трасса")


@pytest.mark.asyncio
async def test_negative_speed():
    with pytest.raises(ValueError, match="Скорость должна быть положительной"):
        await time(100, -10, "трасса")


@pytest.mark.asyncio
async def test_zero_speed():
    with pytest.raises(ValueError, match="Скорость должна быть положительной"):
        await time(100, 0, "трасса")


@pytest.mark.asyncio
async def test_speed_max():
    with pytest.raises(ValueError, match="Скорость не может превышать 150 км/ч"):
        await time(100, 200, "трасса")


@pytest.mark.asyncio
async def test_invalid_terrain_type():
    with pytest.raises(ValueError, match="Тип местности должен быть 'город' или 'трасса'"):
        await time(100, 50, "село")


@pytest.mark.asyncio
async def test_city_speed_limit():
    with pytest.raises(ValueError, match="В городе скорость не может превышать 60 км/ч"):
        await time(100, 70, "город")


@pytest.mark.asyncio
async def test_min_speed():
    result = await time(10, 1, "трасса")
    assert result == 10.0


@pytest.mark.asyncio
async def test_max_speed_highway():
    result = await time(300, 150, "трасса")
    assert result == 2.0


@pytest.mark.asyncio
async def test_city_speed_at_limit():
    result = await time(120, 60, "город")
    assert result == 2.4


@pytest.mark.asyncio
async def test_very_small_speed():
    result = await time(1, 0.1, "трасса")
    assert result == 10.0


@pytest.mark.asyncio
async def test_lab1_edge_cases():
    with pytest.raises(ValueError, match="Скорость не может превышать 150 км/ч"):
        await time(100, 200, "трасса")

    assert await time(0.1, 0.1, "трасса") == 1.0
    assert await time(150, 150, "трасса") == 1.0