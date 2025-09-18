from fastapi import FastAPI
from contextlib import asynccontextmanager


from app.db import create_db_and_tables
from app.api.weather import router as weather_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    create_db_and_tables()
    yield
    # end


app = FastAPI(title="Weather API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


# Router'ı ekle
app.include_router(weather_router)