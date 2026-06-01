from datetime import date, timedelta

from fastapi import APIRouter, Query

from app.services.city_ranking_service import get_ranked_city_scores

router = APIRouter()


@router.get("/cities-scores")
async def get_cities_scores(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
):
    yesterday = date.today() - timedelta(days=1)

    start = start_date or yesterday
    end = end_date or yesterday

    return await get_ranked_city_scores(
        start_date=start,
        end_date=end,
    )