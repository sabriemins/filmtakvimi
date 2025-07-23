from scraper_paribu import get_upcoming_movies
from ics import Calendar, Event
from datetime import datetime
import os

def create_ics_from_movies(movies):
    calendar = Calendar()
    for film in movies:
        try:
            event = Event()
            event.name = film["title"]
            event.begin = datetime.strptime(film["date"], "%Y%m%d")
            event.description = f"▶️ Fragman: {film.get('trailer', 'Yok')}"
            event.location = film["link"]
            calendar.events.add(event)
        except Exception as e:
            print(f"Etkinlik oluşturulamadı: {film['title']}, {e}")
    return calendar

def main():
    movies = get_upcoming_movies()
    calendar = create_ics_from_movies(movies)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "film_takvimi.ics")

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(calendar)

    print(f"ICS dosyası oluşturuldu: {output_path}")

if __name__ == "__main__":
    main()