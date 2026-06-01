from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


async def fake_get_ranked_city_scores(start_date, end_date):
    return [
        {
            "city": "Munich",
            "country": "Germany",
            "score": 9.1,
        },
        {
            "city": "Warsaw",
            "country": "Poland",
            "score": 8.2,
        },
    ]


def test_get_cities_scores_endpoint(monkeypatch):
    monkeypatch.setattr(
        "app.api.v1.cities_scores.get_ranked_city_scores",
        fake_get_ranked_city_scores,
    )

    response = client.get("/api/v1/cities-scores")

    assert response.status_code == 200
    assert response.json() == [
        {
            "city": "Munich",
            "country": "Germany",
            "score": 9.1,
        },
        {
            "city": "Warsaw",
            "country": "Poland",
            "score": 8.2,
        },
    ]