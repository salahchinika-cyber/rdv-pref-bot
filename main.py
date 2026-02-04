import requests
import time
from bs4 import BeautifulSoup

URL = "https://www.rdv-prefecture.interieur.gouv.fr/rdvpref/reservation/demarche/11800/creneau/"
BOT_TOKEN = "8425911873:AAFXQCBvd2Xf4oxNwMMFdIcKSW8cGM3eceE"
CHAT_ID = "1244185550"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload, timeout=20)

def check_slots():
    response = requests.get(URL, timeout=20)
    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text().lower()

    if "aucun créneau disponible" not in page_text:
        send_telegram(
            "🚨 CRÉNEAU DISPONIBLE À LA PRÉFECTURE 🚨\n"
            "👉 https://www.rdv-prefecture.interieur.gouv.fr\n\n"
            "⚡ Clique vite et prends le RDV !"
        )
        return True
    return False

send_telegram("🤖 Surveillance des RDV préfecture ACTIVÉE (check toutes les 60 secondes)")

while True:
    try:
        check_slots()
    except Exception as e:
        print("Erreur:", e)
    time.sleep(60)
