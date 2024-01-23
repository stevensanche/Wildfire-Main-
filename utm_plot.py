"""Plot UTM points on a basemap image.
M Young, 2022-09-17
"""

import graphics.graphics as graphics

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

PT_MARK_SIZE = 3  # pixels

# Contrasty colors for at least 10 groups
COLOR_WHEEL = [
    graphics.color_rgb(255,0,0),
    graphics.color_rgb(0,255,255),
    graphics.color_rgb(127,0,255),
    graphics.color_rgb(127,255,0),
    graphics.color_rgb(255,0,255),
    graphics.color_rgb(255,127,0),
    graphics.color_rgb(0,0,255),
    graphics.color_rgb(0,127,255),
    graphics.color_rgb(50,50,0),
    graphics.color_rgb(255,0,127)
]

next_color = 0
def choose_color() -> object:
    """Returns next color in color wheel,
    cycling around if necessary.
    """
    global next_color
    choice = COLOR_WHEEL[next_color]
    next_color += 1
    if next_color >= len(COLOR_WHEEL):
        next_color = 0
    return choice

class Map:
    """A plot in UTM coordinates with a georeferenced image"""
    def __init__(self, basemap_path: str,
                 window: tuple[int, int],
                 utm_origin: tuple[int, int],
                 utm_ne_extent: tuple[int, int]):
        win_width, win_height = window
        self.win_width, self.win_height = window
        self.utm_origin_easting, self.utm_origin_northing = utm_origin
        self.utm_extent_easting, self.utm_extent_northing = utm_ne_extent
        self.utm_width = self.utm_extent_easting - self.utm_origin_easting
        self.utm_height = self.utm_extent_northing - self.utm_origin_northing
        self.window = graphics.GraphWin(basemap_path, win_width, win_height)
        self.basemap = graphics.Image(graphics.Point(win_width//2, win_height//2), basemap_path)
        self.basemap.draw(self.window)
        # Conversion factor from meters (UTM) to pixels
        self.pixels_per_meter_easting = self.win_width / self.utm_width
        self.pixels_per_meter_northing = self.win_height / self.utm_height
        # Should be very close but not identical
        log.debug(f"Pixels per meter {self.pixels_per_meter_easting}, {self.pixels_per_meter_northing}")


    def pixel_coordinates(self, easting, northing) -> tuple[int, int]:
        """Convert easting, northing to x,y in canvas space"""
        pixel_x = int(self.pixels_per_meter_easting * (easting - self.utm_origin_easting))
        pixel_y = int(self.pixels_per_meter_northing * (northing - self.utm_origin_northing))
        return (pixel_x, pixel_y)

    def plot_point(self, easting, northing, size_px: int=PT_MARK_SIZE, color: str = "red") -> graphics.Circle:
        pixel_x, pixel_y = self.pixel_coordinates(easting, northing)
        symbol = graphics.Circle(graphics.Point(pixel_x, pixel_y), size_px)
        symbol.setFill(color)
        symbol.draw(self.window)
        return symbol

    def move_point(self, symbol: graphics.Circle, new_pos: tuple[int, int]):
        """Move point to new easting, northing"""
        easting, northing = new_pos
        pixel_x, pixel_y = self.pixel_coordinates(easting, northing)
        old_center = symbol.getCenter()
        old_x, old_y = old_center.x, old_center.y
        symbol.move(pixel_x - old_x, pixel_y - old_y)

    def connect_all(self,
             symbol: graphics.Circle,
             group: list[tuple[float, float]]):
        color = choose_color()
        symbol.setFill(color)
        center = symbol.getCenter()
        for easting, northing in group:
            x, y = self.pixel_coordinates(easting, northing)
            ray = graphics.Line(center, graphics.Point(x, y))
            ray.setOutline(color)
            ray.draw(self.window)