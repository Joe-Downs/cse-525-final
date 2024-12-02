from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import board

image = Image.open("gradient.png")

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
#options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'
options.rgb_pins=[
    board.MTX_R1,
    board.MTX_B1,
    board.MTX_G1,
    board.MTX_R2,
    board.MTX_B2,
    board.MTX_G2]

matrix = RGBMatrix(options = options)

# Make image fit our screen.
# image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

matrix.SetImage(image.convert('RGB'))

while True:
    pass
