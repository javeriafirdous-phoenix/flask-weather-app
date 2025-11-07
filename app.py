from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")


app = Flask(__name__)

# Replace with your own API key from https://openweathermap.org/
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if data.get("main"):
            weather_data = {
                "city": city.title(),
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"]
            }
        else:
            weather_data = {"error": "City not found. Try again!"}
    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
