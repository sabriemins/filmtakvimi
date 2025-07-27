from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from scraper_paribu import get_upcoming_movies, generate_ics_file
import os

app = FastAPI()

# Static klasörü varsa mount et, yoksa atla
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates klasörünü tanımla
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/generate")
def generate():
    movies = get_upcoming_movies()
    filepath = generate_ics_file(movies)
    return FileResponse(filepath, filename="film_takvimi.ics", media_type="text/calendar")
