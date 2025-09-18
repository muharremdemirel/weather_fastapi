from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select


from app.db import engine
from app.models import WeatherRecord
from app.services.open_meteo import geocode_city, fetch_current_weather, WeatherError


router = APIRouter(prefix="/weather", tags=["weather"])


@router.post("/fetch", response_model=WeatherRecord, status_code=201)
def fetch_and_store(city: str = Query(..., min_length=1, description="Şehir adi")) -> WeatherRecord:

    """
    Burasi şehrin verisini çeker ve Db ye kaydeder
    """
    try:
        lat, lon, resolved = geocode_city(city)
        cur = fetch_current_weather(lat, lon)
    except WeatherError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Hava servisi hatası: {e}")


    rec = WeatherRecord(
        city=resolved,
        latitude=lat,
        longitude=lon,
        temperature=cur["temperature"],
        windspeed=cur["windspeed"],
        observed_at=datetime.fromisoformat(cur["observed_at"]),
    )
    with Session(engine) as session:
        session.add(rec)
        session.commit()
        session.refresh(rec)
        return rec
    
@router.get("/latest", response_model=WeatherRecord)
def latest(city: str = Query(..., min_length=1)) -> WeatherRecord:
    """
    Veritabanindaki en son kaydi getirir
    """
    with Session(engine) as session:
        stmt = (
            select(WeatherRecord)
            .where(WeatherRecord.city == city)
            .order_by(WeatherRecord.observed_at.desc())
            .limit(1)
        )
    rec = session.exec(stmt).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı. Önce /weather/fetch ile  çağırın.")
    return rec


@router.get("/history", response_model=List[WeatherRecord])
def history(city: str = Query(..., min_length=1), limit: int = Query(10, ge=1, le=100)) -> List[WeatherRecord]:
    with Session(engine) as session:
        stmt = (
            select(WeatherRecord)
            .where(WeatherRecord.city == city)
            .order_by(WeatherRecord.observed_at.desc())
            .limit(limit)
        )

        return session.exec(stmt).all()