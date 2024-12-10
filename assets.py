import math

from PIL import Image, ImageDraw

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


# =================================== Weather ==================================

def get_condition(condition):
    """Returns Image object corresponding to the condition."""
    match condition:
        case Condition.CLEAR_DAY:
            return Image.open(f"{asset_dir}clear-day.png")
        case Condition.CLEAR_NIGHT:
            return Image.open(f"{asset_dir}clear-night.png")
        case Condition.PARTLY_CLOUDY_DAY:
            return Image.open(f"{asset_dir}partly-cloudy-day.png")
        case Condition.PARTLY_CLOUDY_NIGHT:
            return Image.open(f"{asset_dir}partly-cloudy-night.png")
        case Condition.CLOUDY:
            return Image.open(f"{asset_dir}cloudy.png")
        case Condition.RAINY:
            return Image.open(f"{asset_dir}rainy.png")
        case Condition.STORMY:
            return Image.open(f"{asset_dir}stormy.png")
    return

def get_weekday(weekday):
    """Returns Image object corresponding to the weekday."""
    weekday_dir = asset_dir + "weekdays/"
    match weekday:
        case Weekday.MONDAY:
            return Image.open(f"{weekday_dir}M.png")
        case Weekday.TUESDAY:
            return Image.open(f"{weekday_dir}T.png")
        case Weekday.WEDNESDAY:
            return Image.open(f"{weekday_dir}W.png")
        case Weekday.THURSDAY:
            return Image.open(f"{weekday_dir}T.png")
        case Weekday.FRIDAY:
            return Image.open(f"{weekday_dir}F.png")
        case Weekday.SATURDAY:
            return Image.open(f"{weekday_dir}S.png")
        case Weekday.SUNDAY:
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
