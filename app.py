import datetime as dt
import requests

base_url = "http://api.openweathermap.org/data/2.5/weather?"
api_key = "d82a646fba41dcfeebe68f577c763207"
cities = ["Louisville", "Boston", "San Francisco"]
data = {}

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit

for city in cities:
    url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(url).json()

    temp_kelvin = response['main']['temp']
    temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']
    wind_speed = response['wind']['speed']

    data[city] = {
        "Temperature (°F)": f"{temp_fahrenheit:.0f}",
        "Temperature Feels Like (°F)": f"{feels_like_fahrenheit:.0f}",
        "Humidity (%)": humidity,
        "Wind Speed (m/s)": f"{wind_speed:.0f}",
        "Weather Description": description
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