import asyncio
#from rpi_ws281x import Adafruit_NeoPixel

from strip import clear_all, set_colors_all
from utils import create_color_array, RGB
from config import LED_COUNT


def fade_to_frame(base_coloring, present_coloring, fade_rate):
    red, green, blue = base_coloring.red, base_coloring.green, base_coloring.blue

    leds = present_coloring
    leds.red = leds.red + (red - leds.red) * fade_rate
    leds.green = leds.green + (green - leds.green) * fade_rate
    leds.blue = leds.blue + (blue - leds.blue) * fade_rate
    return leds

class LEDConfigurationBase:
    frame = create_color_array(RGB(r=0, g=0, b=0), LED_COUNT)

    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self._stop = False

    def stop(self):
        self._stop = True

    def call_later(self, delay_ms, callback, *args):
        if self._stop:
            return
        self._loop.call_later(delay_ms / 1000, callback, *args) # convert to second

    def draw_frame(self):
        set_colors_all(self.frame)

    def __del__(self):
        clear_all()
        print("I'm fading, Dave.")
