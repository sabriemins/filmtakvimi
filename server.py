from flask import Flask, send_file, render_template_string
import os
import threading
import time
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("""
        <h1>🎮 Film Takvimi Servisi</h1>
        <p>Takvimi indirmek için <a href='/ics'>buraya tıklayın</a>.</p>
    """)

@app.route("/ics")
def get_ics():
    ics_path = os.path.join("output", "film_takvimi.ics")
    if os.path.exists(ics_path):
        return send_file(ics_path, mimetype="text/calendar")
    else:
        return "Takvim dosyası bulunamadı", 404

def background_ics_updater():
    while True:
        try:
            print("🔄 ICS verisi güncelleniyor...")
            subprocess.run(["python", "main.py"])
        except Exception as e:
            print(f"Hata: {e}")
        time.sleep(43200)  # 12 saat

if __name__ == "__main__":
    threading.Thread(target=background_ics_updater, daemon=True).start()
    app.run(host="0.0.0.0", port=8000)
