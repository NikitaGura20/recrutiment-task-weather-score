from datetime import date, timedelta

from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.city_score import CityScoreResponse
from app.services.city_ranking_service import get_ranked_city_scores

router = APIRouter()


@router.get(
    "/cities-scores",
    response_model=list[CityScoreResponse],
)
async def get_cities_scores(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
):
    yesterday = date.today() - timedelta(days=1)

    start = start_date or yesterday
    end = end_date or yesterday

    if start > end:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date cannot be later than end date.",
        )

    return await get_ranked_city_scores(
        start_date=start,
        end_date=end,
    )