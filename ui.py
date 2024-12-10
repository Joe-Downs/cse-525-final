from time import sleep
from datetime import datetime

# from rgbmatrix import RGBMatrix, RGBMatrixOptions
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions

# import board

import assets
import ui_models
from data_models import Condition, WeatherData, StockData
# import stocks
import f1_api

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

weathers = [int] * 5

for i in range(5):
    date = datetime.fromisoformat(f"2024-05-0{i+1}")
    weather = WeatherData(Condition(i + 1), date, location="SDF")
    weathers[i] = weather

# stock_array = []
# for ticker, info in stocks.topStocksDict.items():
#     timeseries = info["History"]["Open"]
#     stock_array.append(StockData(ticker, timeseries))

top_3_drivers_codes = list(map(lambda driver: driver['Driver']['code'], f1_api.get_driver_standings()['DriverStandings'][:3]))
top_3_constructors = list(map(lambda constructor: constructor['Constructor']['name'], f1_api.get_constructor_standings()['ConstructorStandings'][:3]))
print(top_3_drivers_codes)
print(top_3_constructors)

weather_home = ui_models.WeatherScreen(image_file="assets/weather-frame.png", data=weathers)
# stock_home = ui_models.StockScreen(image_file="assets/stock-frame.png", data=stock_array)
f1_home = ui_models.F1Screen(image_file="assets/weather-frame.png", data=(top_3_drivers_codes, top_3_drivers_codes))

weather_home.toggle_selection()
f1_home.toggle_selection()
# weather_home.next_selection()
# weather_home.update_weather(weathers)
# matrix.SetImage(weather_home.image)
# matrix.SetImage(stock_home.image)
matrix.SetImage(f1_home.image)

# while True:
#     pass


for _ in range(100):
    sleep(1)
    # weather_home.next_selection()
    # weather_home.next_selection()
    # weather_home.prev_selection()
    # stock_home.next_selection()
    f1_home.next_selection()
    matrix.SetImage(f1_home.image)
