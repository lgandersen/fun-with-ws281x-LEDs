import asyncio
#from rpi_ws281x import Adafruit_NeoPixel

from strip import clear_all


def fade_to_base_coloring(base_coloring, present_coloring, fade_rate):
    red, green, blue = base_coloring.red, base_coloring.green, base_coloring.blue

    leds = present_coloring
    leds.red = leds.red + (red - leds.red) * fade_rate
    leds.green = leds.green + (green - leds.green) * fade_rate
    leds.blue = leds.blue + (blue - leds.blue) * fade_rate
    return leds

class LEDConfigurationBase:
    def __init__(self, config):
        for option, value in config.items():
            setattr(self, option, value)
        self._loop = asyncio.get_event_loop()
        self._stop = False

    def stop(self):
        self._stop = True

    def call_later(self, delay_ms, callback, *args):
        if self._stop:
            return
        self._loop.call_later(delay_ms / 1000, callback, *args) # convert to second

    def __del__(self):
        clear_all()
        print("I'm fading, Dave.")
