from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from scraper_paribu import get_upcoming_movies, generate_ics_file
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/generate")
def generate():
    movies = get_upcoming_movies()
    generate_ics_file(movies)
    return {"message": "ICS dosyası oluşturuldu."}
