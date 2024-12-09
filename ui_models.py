from PIL import Image, ImageDraw

import assets
from data_models import WeatherData, Weekday, Condition

cache = "__cache__/"

# =============================== Generic Screen ===============================
class _Screen:
    def __init__(self, cache_file, width=64, height=32, image_file=None,
                 origin=(2,2), text_origin=(2,20), padding=2,
                 drawable_origin=(3,3), drawable_area=(58, 26)):
        self.width = width
        self.height = height
        self.filename = image_file
        self.origin = origin
        self.text_origin = text_origin
        self.cached_file = cache_file
        self.padding = padding
        self.selection_mode = False
        self.current_selection = None
        self.drawable_area = drawable_area
        self.drawable_origin = drawable_origin

        if self.filename is None:
            self.image = Image.new('RGBA', (width, height))
        else:
            self.image = Image.open(self.filename)
        return

    def _create_selections(self, origin, offset, num):
        selections = [int] * num
        for i in range(num):
            selections[i] = ((origin[0] + (offset[0]+1) * i), origin[1] + offset[1] * i)
        return selections

    def save_image(self):
        self.image.save(self.filename, "PNG")
        return

    def cache_image(self):
        self.image.save(self.cached_file, "PNG")
        return

    def _clear_image(self):
        self.image = Image.open(self.filename)
        return

    def _reload_image(self):
        self.image = Image.open(self.cached_file)
        return

    def _draw_text(self, text, origin=None, mask=None):
        """Draw text to the screen at origin (or text_origin if not provided)"""
        if origin is None:
            paste_location = self.text_origin
        text_image = assets.get_text_image(text)
        if mask:
            mask = text_image
        self.image.paste(text_image, paste_location, mask=mask)
        return

# ================================ WeatherScreen ===============================
class WeatherScreen(_Screen):
    def __init__(self, data, image_file=None):
        super().__init__(cache_file=f"{cache}weather-home.png", image_file=image_file)
        self.selection_size = (11,17)
        self.selections = self._create_selections(self.origin, (self.selection_size[0], 0), 5)
        print(f"Selections: {self.selections}")
        self.weather_datas = data
        self._draw_weather()
        return

    def _draw_selection(self):
        self._reload_image()
        draw = ImageDraw.Draw(self.image)
        origin = self.selections[self.current_selection]
        end = (origin[0] + self.selection_size[0], origin[1] + self.selection_size[1])
        draw.rectangle([origin, end], outline="#FF0000")
        return

    def _draw_weather(self):
        """Draw the conditons on the screen."""
        self._clear_image()
        for i in range(len(self.selections)):
            data = self.weather_datas[i]
            combined = assets.get_day_condition_image(data.condition, data.weekday)
            self.image.paste(combined, (self.origin[0] + 1 + (combined.width + self.padding) * i, self.origin[1] + 1), mask=combined)
        # We're assuming that the locations are the same for each data point
        self._draw_text(self.weather_datas[0].location, mask=True)
        self.cache_image()
        return

    def _move_selection(self, delta):
        print(f"Current selection = {self.current_selection}")
        self.current_selection = (self.current_selection + delta) % len(self.selections)
        self._draw_selection()
        return

    def next_selection(self):
        self._move_selection(1)
        return

    def prev_selection(self):
        self._move_selection(-1)
        return

    def toggle_selection(self):
        self.selection_mode = not self.selection_mode
        if self.selection_mode:
            self.current_selection = 0
            self._draw_selection()
        else:
            self.current_selection = None
            self._reload_image()
            return

    def update_weather(self, weather_datas):
        self.weather_datas = weather_datas
        self._draw_weather()
        return

# ================================= StockScreen ================================
class StockScreen(_Screen):
    def __init__(self, data, image_file=None):
        super().__init__(cache_file=f"{cache}stock-home.png", image_file=image_file)
        self.stock_data = data
        self._draw_stock()
        return

    def _draw_stock(self):
        graph = assets.get_stock_graph(self.stock_data.data, self.drawable_area[0], self.drawable_area[1])
        self.image.paste(graph, (self.drawable_origin))
        self._draw_text(self.stock_data.ticker)
        self.cache_image()
        return
