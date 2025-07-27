from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
from datetime import datetime
import pytz
from ics import Calendar, Event
import scraper_paribu

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/calendar.ics")
def get_calendar():
    film_listesi = scraper_paribu.scrape()
    calendar = Calendar()

    for film in film_listesi:
        event = Event()
        event.name = film["title"]
        
        # Özet kontrolü
        ozet = film["ozet"] if film["ozet"] else "Özet bulunamadı"

        # Description kısmı
        description = f"""🎬 Tür: {film["tur"]}
📄 Özet: {ozet}
▶️ Fragman: {film["fragman"]}
🔗 Detaylar: {film["link"]}"""
        event.description = description

        # Saat dilimi ayarı
        turkey_tz = pytz.timezone("Europe/Istanbul")
        dt_turkey = datetime.strptime(film["tarih"], "%Y-%m-%d")
        dt_turkey = turkey_tz.localize(dt_turkey.replace(hour=22, minute=0, second=0))
        dt_utc = dt_turkey.astimezone(pytz.utc)
        event.begin = dt_utc.strftime("%Y-%m-%d %H:%M:%S")

        # UID oluştur
        uid = f"{uuid.uuid4()}@{film['title'].lower().replace(' ', '')[:5]}.org"
        event.uid = uid

        # Bildirim 1 gün önceden
        event.alarms = ["-P1D"]

        calendar.events.add(event)

    return Response(str(calendar), media_type="text/calendar")
