from enum import StrEnum


class WeatherField(StrEnum):
    TEMPERATURE = "temperature_2m"
    WIND_SPEED = "wind_speed_10m"
    RELATIVE_HUMIDITY = "relative_humidity_2m"
    CLOUD_COVER = "cloud_cover"