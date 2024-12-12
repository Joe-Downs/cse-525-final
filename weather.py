import datetime as dt
import requests

import airportsdata
from data_models import Condition

base_url = "http://api.openweathermap.org/data/2.5/weather?"
forecast_url = "http://api.openweathermap.org/data/2.5/forecast?"

api_key = "d82a646fba41dcfeebe68f577c763207"
#cities = ["Louisville", "Boston", "San Francisco"]
airports = airportsdata.load('IATA')
cities = ["SDF", "BOS", "SFO", "AMS"]
data = {}

def convert_condition(condition):
    if condition < 200:
        return Condition.UNKNOWN
    elif condition < 300:
        return Condition.STORMY
    elif condition < 600:
        return Condition.RAINY
    elif condition < 700:
        return Condition.SNOWY
    elif condition == 800:
        return Condition.CLEAR_DAY
    elif condition <= 802:
        return Condition.PARTLY_CLOUDY_DAY
    elif condition <= 804:
        return Condition.CLOUDY
    else:
        return Condition.UNKNOWN
    return

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit

def get_lat_lon(airport):
    lat = airports[airport]["lat"]
    lon = airports[airport]["lon"]
    return lat, lon

for city in cities:
    lat, lon = get_lat_lon(city)
    url = f"{base_url}appid={api_key}&lat={lat}&lon={lon}"
    response = requests.get(url).json()
    #print(response)

    temp_kelvin = response['main']['temp']
    temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']
    wind_speed = response['wind']['speed']

    url = f"{forecast_url}appid={api_key}&lat={lat}&lon={lon}"
    response = requests.get(url).json()
    conditions = list()

    today = dt.datetime.now() + dt.timedelta(days=-1)
    #print(response)

    for forecast in response["list"]:
        date = dt.datetime.fromtimestamp(forecast["dt"])
        if date.day == today:
            today = today + dt.timedelta(days=1)
            continue
        conditions.append(convert_condition(forecast["weather"][0]["id"]))

    data[city] = {
        "Temperature (°F)": f"{temp_fahrenheit:.0f}",
        "Temperature Feels Like (°F)": f"{feels_like_fahrenheit:.0f}",
        "Humidity (%)": humidity,
        "Wind Speed (m/s)": f"{wind_speed:.0f}",
        "Weather Description": description,
        "Daily Conditions": conditions
    }

print(data)

city_2 = list(data.keys())[1]
city_2_data = data[city_2]

print(f"Temperature in {city_2}: {city_2_data['Temperature (°F)']} °F")
print(f"Temperature in {city_2} feels like: {city_2_data['Temperature Feels Like (°F)']} °F")
print(f"Humidity in {city_2}: {city_2_data['Humidity (%)']}%")
print(f"Wind Speed in {city_2}: {city_2_data['Wind Speed (m/s)']} m/s")
print(f"General Weather in {city_2}: {city_2_data['Weather Description']}")
print("\n")
