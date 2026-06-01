from dataclasses import dataclass


@dataclass(frozen=True)
class City:
    name: str
    latitude: float
    longitude: float
    country: str


CITIES = [
    City("Warsaw", 52.2297, 21.0122, "Poland"),
    City("Gdansk", 54.3520, 18.6466, "Poland"),
    City("Berlin", 52.5200, 13.4050, "Germany"),
    City("Krakow", 50.0647, 19.9450, "Poland"),
    City("Nurnberg", 49.4521, 11.0767, "Germany"),
    City("Munich", 48.1351, 11.5820, "Germany"),
]