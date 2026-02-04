import pytest
from lab1 import time
def test_1_high():
    result = time(100, 50, "трасса")
    assert result == 2.0  
def test_1_city():
    result = time(60, 30, "город")
    assert result == 2.4
def test_negative():
    with pytest.raises(ValueError, match="Расстояние должно быть положительным"):
        time(-100, 50, "трасса")
def test_zero_distance():
    with pytest.raises(ValueError, match="Расстояние должно быть положительным"):
        time(0, 50, "трасса")
def test_negative_speed():
    with pytest.raises(ValueError, match="Скорость должна быть положительной"):
        time(100, -10, "трасса")
def test_zero_speed():
    with pytest.raises(ValueError, match="Скорость должна быть положительной"):
        time(100, 0, "трасса")
def test_speed_max():
    with pytest.raises(ValueError, match="Скорость не может превышать 150 км/ч"):
        time(100, 200, "трасса")
def test_invalid_terrain_type():
    with pytest.raises(ValueError, match="Тип местности должен быть 'город' или 'трасса'"):
        time(100, 50, "село")
def test_city_speed_limit():
    with pytest.raises(ValueError, match="В городе скорость не может превышать 60 км/ч"):
        time(100, 70, "город")
def test_min_speed():
    result = time(10, 1, "трасса")
    assert result == 10.0
def test_max_speed_highway():
    result = time(300, 150, "трасса")
    assert result == 2.0
def test_city_speed_at_limit():
    result = time(120, 60, "город")
    assert result == 2.4
def test_very_small_speed():
    result = time(1, 0.1, "трасса")
    assert result == 10.0