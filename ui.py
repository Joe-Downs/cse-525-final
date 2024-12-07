from time import sleep

#from rgbmatrix import RGBMatrix, RGBMatrixOptions
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
import board

import ui_models

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

weather_home = ui_models.WeatherScreen(image_file="assets/weather-concept.png")
weather_home.toggle_selection()
weather_home.next_selection()
matrix.SetImage(weather_home.image)
# while True:
#     pass

for _ in range(100):
    sleep(1)
    weather_home.next_selection()
    matrix.SetImage(weather_home.image)
