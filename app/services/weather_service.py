from datetime import date

from fastapi import HTTPException, status
import httpx

from app.constants.open_meteo_data import OpenMeteoParam
from app.core.config import City
from app.constants.weather import WeatherField


OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"


async def fetch_city_weather(
    city: City,
    start_date: date,
    end_date: date,
) -> dict:
    params = {
        OpenMeteoParam.LATITUDE: city.latitude,
        OpenMeteoParam.LONGITUDE: city.longitude,
        OpenMeteoParam.START_DATE: start_date.isoformat(),
        OpenMeteoParam.END_DATE: end_date.isoformat(),
        OpenMeteoParam.HOURLY: ",".join(WeatherField),
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(OPEN_METEO_ARCHIVE_URL, params=params)
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as error:
        if error.response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Weather service is temporarily overloaded. Please try again later.",
            )

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to fetch weather data from external service.",
        )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Weather service did not respond in time. Please try again later.",
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Weather service is currently unavailable. Please try again later.",
        )