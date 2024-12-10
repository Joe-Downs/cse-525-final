import os.path

from PIL import Image, ImageDraw

import assets
from data_models import WeatherData, Weekday, Condition

TEXT_HEIGHT = 9
TEXT_WIDTH = 6

cache = "__cache__/"

# =============================== Generic Screen ===============================
class _Screen:
    def __init__(self, data, cache_file, width=64, height=32, image_file=None,
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
        self.data = data

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

    def cache_image(self, cached_filename=None):
        if cached_filename is None:
            self.image.save(self.cached_file, "PNG")
        else:
            self.image.save(cached_filename, "PNG")
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
        else:
            paste_location = origin
        text_image = assets.get_text_image(text)
        if mask:
            mask = text_image
        self.image.paste(text_image, paste_location, mask=mask)
        return

    def _move_selection(self, delta):
        self._reload_image()
        self.current_selection = (self.current_selection + delta) % len(self.data)
        return

    def next_selection(self):
        self._move_selection(1)
        return

    def prev_selection(self):
        self._move_selection(-1)
        return

# ================================ WeatherScreen ===============================
class WeatherScreen(_Screen):
    def __init__(self, data, image_file=None):
        super().__init__(data=data, cache_file=f"{cache}weather-home.png", image_file=image_file)
        self.selection_size = (11,17)
        self.selections = self._create_selections(self.origin, (self.selection_size[0], 0), 5)
        print(f"Selections: {self.selections}")
        self._draw_weather()
        return

    def _draw_selection(self):
        draw = ImageDraw.Draw(self.image)
        origin = self.selections[self.current_selection]
        end = (origin[0] + self.selection_size[0], origin[1] + self.selection_size[1])
        draw.rectangle([origin, end], outline="#FF0000")
        return

    def _draw_weather(self):
        """Draw the conditons on the screen."""
        self._clear_image()
        for i in range(len(self.selections)):
            data = self.data[i]
            combined = assets.get_day_condition_image(data.condition, data.weekday)
            self.image.paste(combined, (self.origin[0] + 1 + (combined.width + self.padding) * i, self.origin[1] + 1), mask=combined)
        # We're assuming that the locations are the same for each data point
        self._draw_text(self.data[0].location, mask=True)
        self.cache_image()
        return

    def _move_selection(self, delta):
        super()._move_selection(delta)
        #self._draw_selection()
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
        self.data = weather_datas
        self._draw_weather()
        return

# ================================= StockScreen ================================
class StockScreen(_Screen):
    def __init__(self, data, image_file=None):
        super().__init__(data=data, cache_file=f"{cache}stock-home.png", image_file=image_file)
        self.current_selection = 0
        self._draw_stock()
        return

    def _draw_stock(self):
        graph = assets.get_stock_graph(self.data[self.current_selection].time_series, self.drawable_area[0], self.drawable_area[1])
        self.image.paste(graph, (self.drawable_origin))
        ticker = self.data[self.current_selection].ticker
        self._draw_text(ticker)
        self.cache_image(f"{cache}stock-{ticker}.png")
        return

    def _reload_image(self):
        cached_image_path = f"{cache}stock-{self.data[self.current_selection].ticker}.png"
        print(cached_image_path)
        if os.path.exists(cached_image_path):
            self.image = Image.open(cached_image_path)
        else:
            self._draw_stock()
        return

class F1Screen(_Screen):
    def __init__(self, data, image_file=None):
        super().__init__(data=data, cache_file=f"{cache}weather-home.png" ,image_file=image_file)
        self.selection_size = (6, 7)
        self.selections = self._create_selections((self.width // 2 - 10, self.origin[1]+1), (10, 0), 2)
        self.current_selection = 0 # 0 for drivers, 1 for constructors
        self.icons = [assets.get_icon("helmet-orange-thin"), assets.get_icon("car")]
        self._draw_f1()
        return

    def _draw_text(self, text, origin, mask=None):
        """ Draw full "sentences" one letter at a time. """
        for i, char in enumerate(text):
            super()._draw_text(char, (origin[0] + TEXT_WIDTH*i, origin[1]), mask)
        return


    def _draw_selection(self):
        draw = ImageDraw.Draw(self.image)
        origin = self.selections[self.current_selection]
        end = (origin[0] + self.selection_size[0], origin[1] + self.selection_size[1])
        draw.rectangle([origin, end], outline="#FF0000")
        return

    def _draw_f1(self):
        """ Draw helmet and car icons on the screen as well as standings."""
        self._clear_image()
        for i in range(len(self.selections)):
            icon = self.icons[i]
            self.image.paste(icon, self.selections[i], mask=icon)
        self.cache_image()

        self._draw_standings()

        return

    def _move_selection(self, delta):
        super()._move_selection(delta)
        self._draw_f1()
        self._draw_selection()
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

    def _draw_standings(self):
        """ Draw either driver or constructor standings on the screen. (based on current selection)"""
        for i, driver_code in enumerate(self.data[self.current_selection]):
            self._draw_text(driver_code, origin=(self.origin[0], self.origin[1] + 10 + TEXT_HEIGHT*i))

        return
    
