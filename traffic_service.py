import random

class GoogleMapsService:
    async def get_traffic_score(self, route_id: str) -> int:
        return random.randint(0, 10)