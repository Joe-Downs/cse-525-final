from PIL import Image

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
    spread = time_series[height-1] - time_series[0]
    minimum = time_series.min()
    price_range = time_series.max() - minimum
    pixel_scale = price_range / height
    stock_graph = Image.new("RGBA", (width, height), None)
    color = "#00FF00"
    if spread < 0:
        color = "#FF0000"
    for i in range(0,width):
        coord = (i, round((time_series[i] - minimum)/pixel_scale))
        stock_graph.putpixel(coord, color)
    return stock_graph
