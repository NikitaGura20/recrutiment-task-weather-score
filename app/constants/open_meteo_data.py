from enum import StrEnum


class OpenMeteoParam(StrEnum):
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    START_DATE = "start_date"
    END_DATE = "end_date"
    HOURLY = "hourly"