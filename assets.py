from PIL import Image

from data_models import Weekday, Condition

asset_dir = "assets/"

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

def get_location_image(location):
    """Returns image object of letters spelling out location name."""
    letters_dir = asset_dir + "letters/"
    length = len(location)
    height = 9
    width = 5
    loc_image = Image.new("RGBA", ((width+1)*length, height), None)
    for i in range(length):
        letter_image = Image.open(f"{letters_dir}{location[i]}.png")
        loc_image.paste(letter_image, ((width + 1) * i + 1, 0))
    loc_image.save("foo.png")
    return loc_image
