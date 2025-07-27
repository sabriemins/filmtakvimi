from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from scraper_paribu import get_upcoming_movies
from ics import Calendar, Event
from datetime import datetime, timedelta
import os
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/output", StaticFiles(directory="output"), name="output")

def create_ics_from_movies(movies):
    calendar = Calendar()
    for film in movies:
        try:
            event = Event()
            event.name = film["title"]
            event.begin = datetime.strptime(film["date"], "%Y%m%d") + timedelta(hours=19)  # TSI 22:00

            event.description = (
                f"🎬 Tür: {film.get('genre', 'Tür belirtilmemiş')}\n"
                f"📄 Özet: {film.get('summary', 'Özet bulunamadı')}\n"
                f"▶️ Fragman: {film.get('trailer', 'Yok')}\n"
                f"🔗 Detaylar: {film.get('link', '')}"
            )

            # UID benzersiz olsun
            event.uid = f"{uuid.uuid4()}@{uuid.uuid4().hex[:5]}.org"

            # 1 gün önce hatırlatma
            event.alarms = [
                {
                    "action": "display",
                    "trigger": timedelta(days=-1)
                }
            ]

            calendar.events.add(event)
        except Exception as e:
            print(f"Etkinlik oluşturulamadı: {film['title']}, {e}")
    return calendar

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/olustur")
async def generate_calendar():
    movies = get_upcoming_movies()
    calendar = create_ics_from_movies(movies)

    os.makedirs("output", exist_ok=True)
    path = "output/film_takvimi.ics"
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(calendar)

    return FileResponse(path, media_type="text/calendar", filename="film_takvimi.ics")
