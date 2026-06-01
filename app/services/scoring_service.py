from app.constants.open_meteo_data import OpenMeteoParam
from app.constants.weather import WeatherField
from app.constants.scoring import (
    CLOUD_WEIGHT,
    HUMIDITY_DEVIATION_DIVISOR,
    HUMIDITY_WEIGHT,
    IDEAL_CLOUD_COVER,
    IDEAL_HUMIDITY,
    IDEAL_TEMPERATURE,
    MAX_CLOUD_COVER,
    MAX_SCORE,
    TEMPERATURE_WEIGHT,
    WIND_WEIGHT,
)

def calculate_temperature_score(value: float) -> float:
    return max(MAX_SCORE - abs(value - IDEAL_TEMPERATURE), 0)

def calculate_wind_score(value: float) -> float:
    return max(MAX_SCORE - value, 0)


def calculate_humidity_score(value: float) -> float:
    return max(
        MAX_SCORE - abs(value - IDEAL_HUMIDITY) / HUMIDITY_DEVIATION_DIVISOR,
        0,
    )

def calculate_cloud_score(value: float) -> float:
    if value <= IDEAL_CLOUD_COVER:
        return value / IDEAL_CLOUD_COVER * MAX_SCORE

    return max(
        MAX_SCORE
        - (
            (value - IDEAL_CLOUD_COVER)
            / (MAX_CLOUD_COVER - IDEAL_CLOUD_COVER)
            * MAX_SCORE
        ),
        0,
    )

def calculate_hour_score(
    temperature: float,
    wind_speed: float,
    humidity: float,
    cloud_cover: float,
) -> float:
    return (
        calculate_temperature_score(temperature) * TEMPERATURE_WEIGHT
        + calculate_wind_score(wind_speed) * WIND_WEIGHT
        + calculate_humidity_score(humidity) * HUMIDITY_WEIGHT
        + calculate_cloud_score(cloud_cover) * CLOUD_WEIGHT
    )

def calculate_city_score(weather_data: dict) -> float:
    hourly = weather_data[OpenMeteoParam.HOURLY]

    scores = [
        calculate_hour_score(
            temperature=temperature,
            wind_speed=wind_speed,
            humidity=humidity,
            cloud_cover=cloud_cover,
        )
        for temperature, wind_speed, humidity, cloud_cover in zip(
            hourly[WeatherField.TEMPERATURE],
            hourly[WeatherField.WIND_SPEED],
            hourly[WeatherField.RELATIVE_HUMIDITY],
            hourly[WeatherField.CLOUD_COVER],
        )
    ]

    if not scores:
        return 0.0

    return round(sum(scores) / len(scores), 2)