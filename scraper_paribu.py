from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from tqdm import tqdm
import time
import uuid
import os

def get_upcoming_movies():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--log-level=3')

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    base_url = "https://www.paribucineverse.com/gelecek-filmler"
    driver.get(base_url)
    time.sleep(5)

    movie_elements = driver.find_elements(By.CLASS_NAME, "movie-list-banner-item")
    movie_data = []

    for element in tqdm(movie_elements, desc="Film kartları alınıyor"):
        try:
            title = element.find_element(By.CLASS_NAME, "movie-title").text.strip()
            date = element.find_element(By.CLASS_NAME, "movie-date").text.strip()
            link = element.find_element(By.TAG_NAME, "a").get_attribute("href")

            day, month, year = date.split(".")
            iso_date = f"{year}{month}{day}"

            movie_data.append({
                "title": title,
                "date": iso_date,
                "link": link
            })
        except Exception:
            continue

    for movie in tqdm(movie_data, desc="Film detayları alınıyor"):
        try:
            driver.get(movie["link"])
            time.sleep(2)

            try:
                trailer_btn = driver.find_element(By.CLASS_NAME, "video-open-btn")
                movie["trailer"] = trailer_btn.get_attribute("data-trailer-url")
            except:
                movie["trailer"] = "Fragman bağlantısı yok"

            try:
                genre = driver.find_element(By.CSS_SELECTOR, ".item-info.movie-genre small").text.strip()
                movie["genre"] = genre
            except:
                movie["genre"] = "Tür belirtilmemiş"

            try:
                summary_block = driver.find_element(By.CLASS_NAME, "movie-summary-tablet")
                paragraphs = summary_block.find_elements(By.TAG_NAME, "p")
                if paragraphs:
                    movie["summary"] = "\n".join([p.text.strip() for p in paragraphs if p.text.strip()])
                else:
                    movie["summary"] = "Özet bulunamadı"
            except:
                movie["summary"] = "Özet bulunamadı"

        except Exception:
            continue

    driver.quit()
    return movie_data

def generate_ics_file(movies, filename="vizyon_takvimi.ics"):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "PRODID:-//Paribu Cineverse Takvimi//EN"
    ]

    for movie in movies:
        uid = str(uuid.uuid4())
        dtstart = f"{movie['date']}T190000Z"  # Saat 19:00 UTC
        genre = movie.get("genre", "Tür belirtilmemiş")
        summary = movie.get("summary", "Özet bulunamadı")
        trailer = movie.get("trailer", "Fragman bağlantısı yok")
        link = movie.get("link", "")
        description = f"🎬 Tür: {genre}\n📄 Özet: {summary}\n▶️ Fragman: {trailer}\n🔗 Detaylar: {link}"

        event = [
            "BEGIN:VEVENT",
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            "DESCRIPTION:",
            "TRIGGER:-P1D",
            "END:VALARM",
            f"DESCRIPTION:{description}",
            # LOCATION satırı kaldırıldı!
            f"DTSTART:{dtstart}",
            f"SUMMARY:{movie['title']}",
            f"UID:{uid}@{uid[:4]}.org",
            "END:VEVENT"
        ]
        lines.extend(event)

    lines.append("END:VCALENDAR")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n🎉 iCalendar dosyası oluşturuldu: {filename}")

if __name__ == "__main__":
    movies = get_upcoming_movies()
    generate_ics_file(movies)
