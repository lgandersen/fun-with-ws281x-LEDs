import asyncio
from rpi_ws281x import Adafruit_NeoPixel

from config import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, CORD_LED
from utils import create_rgb_array, create_color_array


def color24bit(red, green, blue):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    if CORD_LED:
        return int( (green << 16) | (red << 8) | blue )
    else:
        return int( (red << 16) | (green << 8) | blue )


class LEDConfigurationBase:
    def __init__(self, config):
        for option, value in config.items():
            setattr(self, option, value)
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        self._leds = create_rgb_array((LED_COUNT,))
        self._loop = asyncio.get_event_loop()
        self._stop = False

    def stop(self):
        self._stop = True

    def render(self):
        self.strip.show()

    def call_later(self, delay_ms, callback, *args):
        if self._stop:
            return
        self._loop.call_later(delay_ms / 1000, callback, *args) # convert to second

    def set_color(self, idx, color):
        color24b = color24bit(*color)
        self._leds[idx] = color
        self.strip.setPixelColor(idx, color24b)

    def set_color_all(self, colors):
        if isinstance(colors, tuple) and len(colors) == 3:
            colors = create_color_array(colors, LED_COUNT)

        for n in range(LED_COUNT - 1):
            self.set_color(n, colors[n])
        self.render()

    def clear(self):
        """Wipe color across display a pixel at a time."""
        off = (0, 0, 0)
        for i in range(self.strip.numPixels()):
            self.set_color(i, off)
        self.strip.show()

    def fade_to_basecolor(self, base_color, fade_rate):
        red, green, blue = base_color
        leds = self._leds
        lights2correct = (leds.red != red) | (leds.blue != blue) | (leds.green != green)
        leds.red = leds.red + (red - leds.red) * fade_rate
        leds.green = leds.green + (green - leds.green) * fade_rate
        leds.blue = leds.blue + (blue - leds.blue) * fade_rate
        for n in range(leds.size):
            if lights2correct[n]:
                self.set_color(n, leds[n])
        self.render()
        self.call_later(self.fade_freq, self.fade_to_basecolor, base_color, fade_rate)

    def __del__(self):
        print("I'm fading, Dave.")
