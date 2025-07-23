from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def get_upcoming_movies():
    # Başlangıç driver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    base_url = "https://www.paribucineverse.com/gelecek-filmler"
    driver.get(base_url)
    time.sleep(5)

    movie_elements = driver.find_elements(By.CLASS_NAME, "movie-list-banner-item")

    movie_data = []

    for element in movie_elements:
        try:
            title = element.find_element(By.CLASS_NAME, "movie-title").text.strip()
            date = element.find_element(By.CLASS_NAME, "movie-date").text.strip()
            link = element.find_element(By.TAG_NAME, "a").get_attribute("href")

            # Format tarihi
            day, month, year = date.split(".")
            iso_date = f"{year}{month}{day}"

            movie_data.append({
                "title": title,
                "date": iso_date,
                "link": link
            })
        except Exception as e:
            print("Film kartı işlenemedi:", e)
            continue

    # Şimdi her film sayfasını gezerek fragman al
    for movie in movie_data:
        try:
            driver.get(movie["link"])
            time.sleep(3)

            try:
                video_tag = driver.find_element(By.TAG_NAME, "video")
                trailer_link = video_tag.get_attribute("data-customvideourl")
            except:
                trailer_link = "Fragman bulunamadı"

            movie["trailer"] = trailer_link
        except Exception as e:
            print("Fragman alınamadı:", e)
            movie["trailer"] = "Fragman alınamadı"

    driver.quit()
    return movie_data