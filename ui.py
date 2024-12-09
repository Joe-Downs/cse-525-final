from time import sleep
from datetime import datetime

#from rgbmatrix import RGBMatrix, RGBMatrixOptions
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
import board

import assets
import ui_models
from data_models import Condition

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
 # options.rgb_pins=[
 #     board.MTX_R1,
 #     board.MTX_B1,
 #     board.MTX_G1,
 #     board.MTX_R2,
 #     board.MTX_B2,
 #     board.MTX_G2]

matrix = RGBMatrix(options = options)

weathers = [int] * 5

for i in range(5):
    date = datetime.fromisoformat(f"2024-05-0{i+1}")
    weather = ui_models.WeatherData(Condition(i+1), date)
    weathers[i] = weather

weather_home = ui_models.WeatherScreen(image_file="assets/weather-frame.png", data=weathers)

weather_home.toggle_selection()
#weather_home.next_selection()
#weather_home.update_weather(weathers)
matrix.SetImage(weather_home.image)
# while True:
#     pass

for _ in range(100):
    sleep(1)
    weather_home.next_selection()
    #weather_home.next_selection()
    #weather_home.prev_selection()
    matrix.SetImage(weather_home.image)
