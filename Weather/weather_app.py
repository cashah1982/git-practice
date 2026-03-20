from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

#API_KEY = os.environ.get("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")
API_KEY = "3128ca315da229a9370fd9c6606f7277"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str) -> dict | None:
    try:
        resp = requests.get(BASE_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric",
        }, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        weather = data["weather"][0]
        main = data["main"]
        wind = data["wind"]
        return {
            "city":        data["name"],
            "country":     data["sys"]["country"],
            "description": weather["description"].title(),
            "icon":        weather["icon"],
            "temp":        round(main["temp"]),
            "feels_like":  round(main["feels_like"]),
            "humidity":    main["humidity"],
            "wind_speed":  round(wind["speed"] * 3.6),  # m/s → km/h
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": f'City "{city}" not found.'}
        if e.response.status_code == 401:
            return {"error": "Invalid API key. Set the OPENWEATHER_API_KEY environment variable."}
        return {"error": "Weather service error. Please try again."}
    except requests.exceptions.RequestException:
        return {"error": "Could not reach the weather service. Check your connection."}


@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    city = ""
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if city:
            weather = get_weather(city)
    return render_template("index.html", weather=weather, city=city)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
