from flask import Flask, send_file, render_template_string
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("""
        <h1>🎬 Film Takvimi Servisi</h1>
        <p>Takvimi indirmek için <a href='/ics'>buraya tıklayın</a>.</p>
    """)

@app.route("/ics")
def get_ics():
    ics_path = os.path.join("output", "film_takvimi.ics")
    if os.path.exists(ics_path):
        return send_file(ics_path, mimetype="text/calendar")
    else:
        return "Takvim dosyası bulunamadı", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
