import math

from PIL import Image, ImageDraw, ImageFont

from data_models import Weekday, Condition

asset_dir = "assets/"

# =================================== Shared ===================================
def get_text_image(text):
    """Returns image object of letters spelling out text name."""
    letters_dir = asset_dir + "letters/"
    length = len(text)
    height = 9
    width = 5
    loc_image = Image.new("RGBA", ((width+1)*length, height), None)
    for i in range(length):
        letter_image = Image.open(f"{letters_dir}{text[i]}.png")
        loc_image.paste(letter_image, ((width + 1) * i + 1, 0))
    return loc_image

def get_letter_from_atlas(letter):
    """Returns image object of letter from atlas."""
    letter_width = 3
    letter_height = 5
    cols = 6
    padX, padY = 3, 1

    atlas = Image.open(f"{asset_dir}atlas.png")
    letter = letter.upper()
    if letter == " ":
        return Image.new("RGBA", (letter_width, letter_height), None)
    if letter.isdigit():
        letter_index = ord(letter) - 22 
    else:
        letter_index = ord(letter) - 65
    # print("Gettnig letter", letter, letter_index)
    u = letter_index % cols
    v = letter_index // cols
    x = u * (letter_width + padX)
    y = v * (letter_height + padY)

    letter_image = atlas.crop((x, y, x + letter_width, y + letter_height))

    # # save image to assets/temp 
    # letter_image.save(f"{asset_dir}temp/{letter}.png")
    # print(f"U: {u}, V: {v}")
    # print(f"X: {x}, Y: {y}")

    # # input("Press enter to continue")

    return letter_image

def create_atlas():
    # TODO: doesnt work
    # Create a new blank image for the atlas
    letter_width = 6
    letter_height = 6
    columns = 6
    rows = 5
    atlas_width = columns * letter_width
    atlas_height = rows * letter_height
    atlas = Image.new("RGBA", (atlas_width, atlas_height), (255, 255, 255, 0))

    # Load a font
    font = ImageFont.truetype("arial.ttf", 5)

    # Draw each letter onto the atlas
    draw = ImageDraw.Draw(atlas)
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i, letter in enumerate(letters):
        x = (i % columns) * letter_width
        y = (i // columns) * letter_height
        draw.text((x, y), letter, font=font, fill=(0, 0, 0, 255))

    # Save the atlas image
    atlas.save("letters.png")

# =================================== Weather ==================================

def get_condition(condition):
    """Returns Image object corresponding to the condition."""
    if condition==Condition.CLEAR_DAY:
        return Image.open(f"{asset_dir}clear-day.png")
    if condition==Condition.CLEAR_NIGHT:
        return Image.open(f"{asset_dir}clear-night.png")
    if condition==Condition.PARTLY_CLOUDY_DAY:
        return Image.open(f"{asset_dir}partly-cloudy-day.png")
    if condition==Condition.PARTLY_CLOUDY_NIGHT:
        return Image.open(f"{asset_dir}partly-cloudy-night.png")
    if condition==Condition.CLOUDY:
        return Image.open(f"{asset_dir}cloudy.png")
    if condition==Condition.RAINY:
        return Image.open(f"{asset_dir}rainy.png")
    if condition==Condition.STORMY:
        return Image.open(f"{asset_dir}stormy.png")
    return

def get_weekday(weekday):
    """Returns Image object corresponding to the weekday."""
    weekday_dir = asset_dir + "weekdays/"
    if weekday==Weekday.MONDAY:
        return Image.open(f"{weekday_dir}M.png")
    if weekday==Weekday.TUESDAY:
        return Image.open(f"{weekday_dir}T.png")
    if weekday==Weekday.WEDNESDAY:
        return Image.open(f"{weekday_dir}W.png")
    if weekday==Weekday.THURSDAY:
        return Image.open(f"{weekday_dir}T.png")
    if weekday==Weekday.FRIDAY:
        return Image.open(f"{weekday_dir}F.png")
    if weekday==Weekday.SATURDAY:
        return Image.open(f"{weekday_dir}S.png")
    if weekday==Weekday.SUNDAY:
        return Image.open(f"{weekday_dir}S.png")
    return

def get_day_condition_image(condition, weekday):
    condition_image = get_condition(condition)
    weekday_image = get_weekday(weekday)
    width = condition_image.width
    # 1 pixel of padding between weekday and condition images
    height = condition_image.height + weekday_image.height + 1
    combined = Image.new("RGBA", (width, height), None)
    combined.paste(condition_image, (0,0))
    combined.paste(weekday_image, (0,condition_image.height+1))
    return combined

# =================================== Stocks ===================================
def get_stock_graph(time_series, width, height):
    time_series = time_series[-width::]
    spread = time_series.iloc[-1] - time_series.iloc[0]
    minimum = time_series.min()
    price_range = time_series.max() - minimum
    pixel_scale = price_range / (height - 1)
    stock_graph = Image.new("RGBA", (width, height), None)
    draw = ImageDraw.Draw(stock_graph)
    color = (0, 255, 0)
    if spread < 0:
        color = (255, 0, 0)

    def _calculate_pixel_y(value):
        return math.floor((value - minimum)/pixel_scale)
    prev_value = _calculate_pixel_y(time_series.iloc[-1])
    stock_graph.putpixel((0, prev_value), color)

    for i in range(1, width):
        coord = (i, _calculate_pixel_y(time_series.iloc[-i-1]))
        if coord[1] > prev_value + 1:
            draw.line((coord, (i, prev_value+1)), fill=color)
        elif coord[1] < prev_value - 1:
            draw.line((coord, (i, prev_value-1)), fill=color)
        else:
            stock_graph.putpixel(coord, color)
        prev_value = coord[1]
    return stock_graph


# =================================== F1 =======================================
def get_icon(icon_name):
    """Returns the icon image."""
    return Image.open(f"{asset_dir}f1-icons/{icon_name}.png")
