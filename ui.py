from time import sleep
from datetime import datetime, timedelta

from rgbmatrix import RGBMatrix, RGBMatrixOptions
#from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions

import assets
import ui_models
from data_models import WeatherData, StockData
import stocks
import f1_api
import weather
from weather import data


# ================================ Button Setup ================================
import board
import digitalio

buttons = []

enter_button = digitalio.DigitalInOut(board.C0)
buttons.append(enter_button)
next_button = digitalio.DigitalInOut(board.C1)
buttons.append(next_button)
prev_button = digitalio.DigitalInOut(board.C2)
buttons.append(prev_button)

selection = 0

for button in buttons:
    button.direction = digitalio.Direction.INPUT

# ================================ Matrix Setup ================================
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat"  # If you have an Adafruit HAT: 'adafruit-hat'
# options.rgb_pins=[
#     board.MTX_R1,
#     board.MTX_B1,
#     board.MTX_G1,
#     board.MTX_R2,
#     board.MTX_B2,
#     board.MTX_G2]

matrix = RGBMatrix(options=options)

# =============================== Data Collection ==============================
weather_array = list()

for city in weather.cities:
    city_data = data[city]
    date = datetime.now()
    conditions = list()
    for condition in city_data["Daily Conditions"]:
        weather = WeatherData(condition, date, location=city)
        date = date + timedelta(days=1)
        conditions.append(weather)
    weather_array.append(conditions)

stock_array = []
for ticker, info in stocks.topStocksDict.items():
    timeseries = info["History"]["Open"]
    stock_array.append(StockData(ticker, timeseries))

driver_standings = f1_api.get_driver_standings(1978)['DriverStandings']
constructor_standings = f1_api.get_constructor_standings(1978)['ConstructorStandings']
top_3_drivers = list(map(lambda driver: (driver['Driver'].get('code', driver['Driver']['familyName'][:3]), driver['points']), driver_standings[:3]))
top_3_constructors = list(map(lambda constructor: (f1_api.constructor_name_to_id.get(constructor['Constructor']['constructorId'], constructor['Constructor']['name'][:3]), constructor['points']), constructor_standings[:3]))
print(top_3_drivers)
print(top_3_constructors)

weather_screen = ui_models.WeatherScreen(image_file="assets/weather-frame.png", data=weather_array)
stock_screen = ui_models.StockScreen(image_file="assets/stock-frame.png", data=stock_array)
f1_screen = ui_models.F1Screen(image_file="assets/f1-frame.png", data=(top_3_drivers, top_3_constructors))

selections = [weather_screen, stock_screen, f1_screen]

primary_selection = True
secondary_selection = False
while True:
    if primary_selection:
        if next_button.value:
            selection += 1
            selection = selection % len(selections)
        elif prev_button.value:
            selection -= 1
            selection = selection % len(selections)
    else:
        if next_button.value:
            selections[selection].next_selection()
        elif prev_button.value:
            selections[selection].prev_selection()
    if enter_button.value:
        selections[selection].toggle_selection()
        secondary_selection = not secondary_selection
        primary_selection = not primary_selection
    sleep(0.1)
    matrix.SetImage(selections[selection].image.convert('RGB'))
