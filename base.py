import asyncio

from strip import clear_all, set_colors_all
from utils import create_color_array, RGB
from config import LED_COUNT


def morph_frame(base_frame, frame2morph, fade_rate):
    red, green, blue = base_frame.red, base_frame.green, base_frame.blue

    frame2morph.red = frame2morph.red + (red - frame2morph.red) * fade_rate
    frame2morph.green = frame2morph.green + (green - frame2morph.green) * fade_rate
    frame2morph.blue = frame2morph.blue + (blue - frame2morph.blue) * fade_rate
    return frame2morph

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
