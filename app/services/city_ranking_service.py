import asyncio
from datetime import date

from app.cache.decorators import cached
from app.core.config import CITIES, City
from app.schemas.city_score import CityScoreResponse
from app.services.scoring_service import calculate_city_score
from app.services.weather_service import fetch_city_weather

MAX_CONCURRENT_REQUESTS = 5


async def fetch_city_weather_limited(
    city: City,
    start_date: date,
    end_date: date,
    semaphore: asyncio.Semaphore,
) -> dict:
    async with semaphore:
        return await fetch_city_weather(
            city=city,
            start_date=start_date,
            end_date=end_date,
        )

@cached
async def get_ranked_city_scores(
    start_date: date,
    end_date: date,
) -> list[CityScoreResponse]:
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    weather_results = await asyncio.gather(
        *[
            fetch_city_weather_limited(
                city=city,
                start_date=start_date,
                end_date=end_date,
                semaphore=semaphore,
            )
            for city in CITIES
        ]
    )

    cities_scores = [
        CityScoreResponse(
            city=city.name,
            country=city.country,
            score=calculate_city_score(weather_data),
        )
        for city, weather_data in zip(CITIES, weather_results)
    ]

    return sorted(
        cities_scores,
        key=lambda city_score: city_score.score,
        reverse=True,
    )