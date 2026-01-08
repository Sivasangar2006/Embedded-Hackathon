import requests

USER_KEY = "u5ejcogtoxyprfzssq31dezy7p49mp"
APP_TOKEN = "ag2yy12xfxs7dni5pg21trnzmyvprc"

r = requests.post(
    "https://api.pushover.net/1/messages.json",
    data={
        "token": APP_TOKEN,
        "user": USER_KEY,
        "title": "Hackathon Test",
        "message": "🚨 Burglary alert system is LIVE!"
    },
    timeout=5
)

print(r.status_code, r.text)
