from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from scraper_paribu import get_film_data
from ics import Calendar, Event, DisplayAlarm
from datetime import datetime, time
import uuid
import os

app = FastAPI()

# Klasör bağlantıları
templates = Jinja2Templates(directory="templates")
app.mount("/output", StaticFiles(directory="output"), name="output")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/olustur")
async def takvim_olustur():
    films = get_film_data()

    calendar = Calendar()

    for film in films:
        if not film["tarih"]:
            continue

        event = Event()
        event.name = film["baslik"]
        event.begin = datetime.combine(film["tarih"], time(19, 0)).strftime("%Y-%m-%dT%H:%M:%SZ")

        fragman = film["fragman"] if film["fragman"] else "Fragman bulunamadı"
        ozet = film["ozet"] if film["ozet"] else "Özet bulunamadı"

        event.description = (
            f"🎮 Tür: {film['tur']}\n"
            f"📄 Özet: {ozet}\n"
            f"▶️ Fragman: {fragman}\n"
            f"🔗 Detaylar: {film['link']}"
        )

        event.uid = f"{uuid.uuid4()}@{uuid.uuid4().hex[:4]}.org"

        # Bildirim: 1 gün önce
        alarm = DisplayAlarm(trigger="-P1D")
        event.alarms = [alarm]

        calendar.events.add(event)

    # Takvimi kaydet
    os.makedirs("output", exist_ok=True)
    with open("output/film_takvimi.ics", "w", encoding="utf-8") as f:
        f.writelines(calendar)

    return {"status": "Takvim başarıyla oluşturuldu.", "film_sayisi": len(films)}
