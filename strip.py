# pylint: disable=I1101, W0212
import numpy as np

from rpi_ws281x import Adafruit_NeoPixel
import _rpi_ws281x as ws

from config import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, WS2811

_strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
_strip.begin()
channel = _strip._channel

shift16 = np.zeros((LED_COUNT,), dtype='int') + 16
shift8 = np.zeros((LED_COUNT,), dtype='int') + 8
color24b = np.zeros((LED_COUNT,), dtype='int')

def _color24bit_all(colors):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    if WS2811:
        color24b[:] = np.left_shift(colors.green, shift16) | np.left_shift(colors.red, shift8) | colors.blue
    else:
        color24b[:] = np.left_shift(colors.red, shift16) | np.left_shift(colors.green, shift8) | colors.blue
    return color24b


def set_colors_all(colors):
    colors24bit = _color24bit_all(colors)
    for n, color in enumerate(colors24bit.tolist()):
        ws.ws2811_led_set(channel, n, color)
    _strip.show()

def clear_all():
    for n, color in enumerate(color24b.tolist()):
        _strip.setPixelColor(n, color)
    _strip.show()
