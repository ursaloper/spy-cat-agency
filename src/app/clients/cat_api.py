from datetime import datetime, timedelta

import httpx

from ..settings import get_settings


class BreedCache:
    def __init__(self, ttl_seconds: int = 300) -> None:
        self.ttl = timedelta(seconds=ttl_seconds)
        self.breeds: list[str] = []
        self.fetched_at: datetime | None = None

    def is_fresh(self) -> bool:
        if self.fetched_at is None:
            return False
        return datetime.utcnow() - self.fetched_at < self.ttl

    def update(self, breeds: list[str]) -> None:
        self.breeds = breeds
        self.fetched_at = datetime.utcnow()


breed_cache = BreedCache()


async def fetch_breeds() -> list[str]:
    settings = get_settings()
    base_url = settings.cat_api_base_url or "https://api.thecatapi.com/v1"
    url = f"{base_url}/breeds"
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
    return [item.get("name", "") for item in data if "name" in item]


async def validate_breed(breed: str) -> bool:
    if not breed_cache.is_fresh():
        breeds = await fetch_breeds()
        breed_cache.update(breeds)
    else:
        breeds = breed_cache.breeds
    return breed.lower() in {b.lower() for b in breeds}
