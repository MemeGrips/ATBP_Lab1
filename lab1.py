def time(distance_km: float, speed_kmh: float, terrain_type: str) -> float:
    if distance_km <= 0:
        raise ValueError("Расстояние должно быть положительным")
    if speed_kmh <= 0:
        raise ValueError("Скорость должна быть положительной")
    if speed_kmh > 150:
        raise ValueError("Скорость не может превышать 150 км/ч")
    if terrain_type not in ["город", "трасса"]:
        raise ValueError("Тип местности должен быть 'город' или 'трасса'")
    if terrain_type == "город" and speed_kmh > 60:
        raise ValueError("В городе скорость не может превышать 60 км/ч")
    time_hours = distance_km / speed_kmh

    if terrain_type == "город":
        time_hours *= 1.2

    return round(time_hours, 2)