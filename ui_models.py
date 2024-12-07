from PIL import Image, ImageDraw, ImageColor

class _Screen:
    def __init__(self, width=64, height=32, image_file=None):
        self.width = width
        self.height = height
        self.filename = image_file
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

    def saveImage(self):
        self.image.save(self.filename, "PNG")
        return

class WeatherScreen(_Screen):
    def __init__(self, image_file=None):
        super().__init__(image_file=image_file)
        self.selection_size = (11,17)
        self.selections = self._create_selections((2,2), (self.selection_size[0], 0), 5)
        print(f"Selections: {self.selections}")
        self.current_selection = None
        self.selection_mode = False
        return

    def _draw_selection(self):
        self._reload_image()
        draw = ImageDraw.Draw(self.image)
        origin = self.selections[self.current_selection]
        end = (origin[0] + self.selection_size[0], origin[1] + self.selection_size[1])
        draw.rectangle([origin, end], outline="#FF0000")
        return

    def _reload_image(self):
        self.image = Image.open(self.filename)
        return

    def _move_selection(self, delta):
        print(f"Current selection = {self.current_selection}")
        self.current_selection = (self.current_selection + 1) % len(self.selections)
        self._draw_selection()
        return

    def next_selection(self):
        self._move_selection(1)
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
