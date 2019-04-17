import numpy as np
from rpi_ws281x import Adafruit_NeoPixel
from config import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, CORD_LED
from utils import create_rgb_array


_strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
_strip.begin()

shift16 = np.zeros((LED_COUNT,), dtype='int') + 16
shift8 = np.zeros((LED_COUNT,), dtype='int') + 8
color24b = np.zeros((LED_COUNT,), dtype='int')

def _color24bit_all(colors):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    if CORD_LED:
        color24b[:] = np.left_shift(colors.green, shift16) | np.left_shift(colors.red, shift8) | colors.blue
    else:
        color24b[:] = np.left_shift(colors.red, shift16) | np.left_shift(colors.green, shift8) | colors.blue
    return color24b


def _color24bit(colors):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    shift16 = np.zeros(colors.shape, dtype='int') + 16
    shift8 = np.zeros(colors.shape, dtype='int') + 8
    color24b = np.zeros(colors.shape, dtype='int')
    if CORD_LED:
        color24b[:] = np.left_shift(colors.green, shift16) | np.left_shift(colors.red, shift8) | colors.blue
    else:
        color24b[:] = np.left_shift(colors.red, shift16) | np.left_shift(colors.green, shift8) | colors.blue
    return color24b


def set_colors_all(colors):
    color24b = _color24bit_all(colors)
    for n, color in enumerate(color24b.tolist()):
        _strip.setPixelColor(n, color)
    _strip.show()

def set_colors(idx, colors):
    color24b = _color24bit(colors)
    for idx, color in zip(idx.tolist(), color24b.tolist()):
        _strip.setPixelColor(idx, color)
    _strip.show()

def clear_all():
    colors = create_rgb_array((LED_COUNT, ))
    color24b = _color24bit_all(colors)
    for n, color in enumerate(color24b.tolist()):
        _strip.setPixelColor(n, color)
    _strip.show()
