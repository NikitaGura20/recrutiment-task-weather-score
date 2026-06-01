from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.cities_scores import router as cities_router


app = FastAPI(title="Weather Score API")

app.include_router(
    cities_router,
    prefix="/api/v1",
    tags=["Cities Scores"],
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)


@app.get("/")
def root():
    return FileResponse("app/static/index.html")