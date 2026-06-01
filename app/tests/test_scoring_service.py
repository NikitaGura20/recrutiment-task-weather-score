from app.constants.open_meteo_data import OpenMeteoParam
from app.constants.weather import WeatherField
from app.services.scoring_service import (
    calculate_city_score,
    calculate_cloud_score,
    calculate_hour_score,
    calculate_humidity_score,
    calculate_temperature_score,
    calculate_wind_score,
)


def test_temperature_score_is_max_when_temperature_is_ideal():
    assert calculate_temperature_score(24) == 10


def test_temperature_score_decreases_by_deviation():
    assert calculate_temperature_score(20) == 6


def test_temperature_score_is_not_negative():
    assert calculate_temperature_score(0) == 0


def test_wind_score_is_max_when_wind_is_zero():
    assert calculate_wind_score(0) == 10


def test_wind_score_decreases_when_wind_increases():
    assert calculate_wind_score(3) == 7


def test_wind_score_is_not_negative():
    assert calculate_wind_score(20) == 0


def test_humidity_score_is_max_when_humidity_is_ideal():
    assert calculate_humidity_score(50) == 10


def test_humidity_score_is_zero_on_extremes():
    assert calculate_humidity_score(0) == 0
    assert calculate_humidity_score(100) == 0


def test_cloud_score_is_max_when_cloud_cover_is_ideal():
    assert calculate_cloud_score(25) == 10


def test_cloud_score_is_zero_on_extremes():
    assert calculate_cloud_score(0) == 0
    assert calculate_cloud_score(100) == 0


def test_hour_score_calculates_weighted_average():
    assert calculate_hour_score(
        temperature=24,
        wind_speed=0,
        humidity=50,
        cloud_cover=25,
    ) == 10


def test_city_score_returns_average_score_for_hourly_data():
    weather_data = {
        OpenMeteoParam.HOURLY: {
            WeatherField.TEMPERATURE: [24, 20],
            WeatherField.WIND_SPEED: [0, 5],
            WeatherField.RELATIVE_HUMIDITY: [50, 75],
            WeatherField.CLOUD_COVER: [25, 100],
        }
    }

    assert calculate_city_score(weather_data) == 7.05


def test_city_score_returns_zero_when_no_hourly_data():
    weather_data = {
        OpenMeteoParam.HOURLY: {
            WeatherField.TEMPERATURE: [],
            WeatherField.WIND_SPEED: [],
            WeatherField.RELATIVE_HUMIDITY: [],
            WeatherField.CLOUD_COVER: [],
        }
    }

    assert calculate_city_score(weather_data) == 0.0