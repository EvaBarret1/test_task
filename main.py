from flask import Flask
import requests

app = Flask(__name__)

def fetch_weather(city):
    url = f"https://api.gismeteo.net/v2/weather/current/{city}/"
    headers = {
        "X-Gismeteo-Token": "YOUR_API_TOKEN",
        "Accept-Encoding": "gzip, deflate"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()

        kind = data.get("kind")
        if kind == "Obs":
            temperature = data.get("temperature").get("air").get("C")
            return temperature
        else:
            return None
    else:
        return None

@app.route('/get_weather/<city>')
def get_weather(city):
    temperature = fetch_weather(city)

    if temperature is not None:
        return f"Температура в городе {city}: {temperature}°C"
    else:
        return f"Не удалось получить данные о погоде для города {city}"

if __name__ == '__main__':
    app.run()
