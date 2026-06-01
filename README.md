# Weather Score App

Fullstack FastAPI application that retrieves historical weather data from the Open-Meteo API and ranks predefined cities based on a custom weather scoring algorithm.

## Features

* Fetches hourly weather data from Open-Meteo
* Supports custom `start_date` and `end_date`
* Defaults to yesterday when dates are not provided
* Calculates weather score for each city
* Returns cities sorted from best to worst weather
* Includes simple HTML/CSS/JS frontend
* Includes in-memory caching for 24 hours
* Includes unit tests
* Docker support included

## Cities

The application compares the following cities:

* Warsaw, Poland
* Gdansk, Poland
* Berlin, Germany
* Krakow, Poland
* Nurnberg, Germany
* Munich, Germany

## Tech Stack

* Python
* FastAPI
* HTTPX
* Pydantic
* Pytest
* Docker
* HTML / CSS / JavaScript

## Project Structure

```text
weather-score-app/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── cities_scores.py
│   ├── cache/
│   │   ├── decorators.py
│   │   └── memory_cache.py
│   ├── constants/
│   │   ├── open_meteo_data.py
│   │   ├── scoring.py
│   │   └── weather.py
│   ├── core/
│   │   └── config.py
│   ├── schemas/
│   │   └── city_score.py
│   ├── services/
│   │   ├── city_ranking_service.py
│   │   ├── scoring_service.py
│   │   └── weather_service.py
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   ├── js/
│   │   │   └── app.js
│   │   └── index.html
│   └── main.py
├── tests/
│   ├── test_cities_scores_endpoint.py
│   └── test_scoring_service.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

## How to Run Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd weather-score-app
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate virtual environment

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python -m uvicorn app.main:app --reload
```

Application:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## How to Run with Docker

### Build and run

```bash
docker compose up --build
```

Application will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

### Stop Docker container

```bash
Ctrl + C
```

or:

```bash
docker compose down
```

## API Endpoint

### Get city weather scores

```http
GET /api/v1/cities-scores
```

### Query Parameters

| Parameter    | Required | Description                       |
| ------------ | -------: | --------------------------------- |
| `start_date` |       No | Start date in `YYYY-MM-DD` format |
| `end_date`   |       No | End date in `YYYY-MM-DD` format   |

If dates are not provided, the application uses yesterday as the default date.

### Example Request

```http
GET /api/v1/cities-scores?start_date=2025-05-01&end_date=2025-05-07
```

### Example Response

```json
[
  {
    "city": "Munich",
    "country": "Germany",
    "score": 8.45
  },
  {
    "city": "Warsaw",
    "country": "Poland",
    "score": 7.91
  }
]
```

## Scoring Algorithm

Open-Meteo provides hourly weather data.
The application calculates a score for every hour and then averages all hourly scores for the selected date range.

Final city score:

```text
city_score = average(hourly_scores)
```

Each hourly score is calculated using four weather parameters:

```text
hour_score =
    temperature_score * 0.35
    + wind_score * 0.20
    + humidity_score * 0.20
    + cloud_score * 0.25
```

## Temperature Score

Field:

```text
temperature_2m
```

Rules:

* 24°C is the best value
* 24°C gives 10 points
* Every 1°C deviation decreases the score by 1 point
* Minimum score is 0

Formula:

```text
temperature_score = max(10 - abs(temperature - 24), 0)
```

Examples:

| Temperature | Score |
| ----------: | ----: |
|        24°C |    10 |
|        23°C |     9 |
|        20°C |     6 |
|        14°C |     0 |
|        34°C |     0 |

## Wind Speed Score

Field:

```text
wind_speed_10m
```

Rules:

* Lower wind speed is better
* 0 gives 10 points
* Every wind speed unit decreases the score by 1 point
* Minimum score is 0

Formula:

```text
wind_score = max(10 - wind_speed, 0)
```

Examples:

| Wind Speed | Score |
| ---------: | ----: |
|          0 |    10 |
|          3 |     7 |
|          5 |     5 |
|         10 |     0 |
|         20 |     0 |

## Relative Humidity Score

Field:

```text
relative_humidity_2m
```

Rules:

* 50% is the best value
* 50% gives 10 points
* 0% and 100% give 0 points
* Score decreases linearly as humidity moves away from 50%

Formula:

```text
humidity_score = max(10 - abs(humidity - 50) / 5, 0)
```

Examples:

| Humidity | Score |
| -------: | ----: |
|      50% |    10 |
|      75% |     5 |
|      25% |     5 |
|       0% |     0 |
|     100% |     0 |

## Cloud Cover Score

Field:

```text
cloud_cover
```

Rules:

* 25% cloud cover is the best value
* 25% gives 10 points
* 0% gives 0 points
* 100% gives 0 points
* Score grows linearly from 0% to 25%
* Score decreases linearly from 25% to 100%

Formula for values from 0 to 25:

```text
cloud_score = cloud_cover / 25 * 10
```

Formula for values from 25 to 100:

```text
cloud_score = max(10 - ((cloud_cover - 25) / 75 * 10), 0)
```

Examples:

| Cloud Cover | Score |
| ----------: | ----: |
|          0% |     0 |
|         25% |    10 |
|         50% |  6.67 |
|         75% |  3.33 |
|        100% |     0 |

## Caching

City ranking results are cached in memory for 24 hours.

The cache key is based on the requested date range:

```text
start_date:end_date
```

This reduces repeated requests to the Open-Meteo API and helps avoid rate limiting.

## Error Handling

The application handles errors from the external weather API and returns user-friendly messages for:

* Weather service unavailable
* Request timeout
* Too many requests
* Failed external API response

The frontend displays these errors in a readable format.

## Run Tests

```bash
python -m pytest -v
```

The project includes tests for:

* scoring functions
* city score calculation
* `/api/v1/cities-scores` endpoint

## Notes

The Open-Meteo API provides hourly data.
This implementation calculates a weighted weather score for each hour and then averages all hourly scores across the selected date range to produce the final city ranking.
