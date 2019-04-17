import time
import random
from collections import namedtuple
import numpy as np

from config import LED_COUNT

RGB = namedtuple('RGB', ['r', 'g', 'b'])

rgb_type = np.dtype([('red', 'int'), ('green', 'int'), ('blue', 'int')])


def create_rgb_array(shape):
    if isinstance(shape, int):
        array = np.zeros((shape,), dtype=rgb_type)
    else:
        array = np.zeros(shape, dtype=rgb_type)
    return array.view(np.recarray)


def sleep_ms(ms):
    time.sleep(ms/1000.0)


def random_color(colors):
    idx = random.randint(0, colors.shape[0] - 1)
    return colors[idx]


def create_color_array(cmap, length):
    color_array = create_rgb_array((length,))
    # Pseudo-cmap made from strandtest.py rainbow-function
    if cmap == 'strandtest_rainbow':
        pos = np.linspace(0, 255, length, dtype='int')
        for idx in range(len(pos)):
            color_array[idx] = _rainbow(pos[idx])

    # A tuple of length 3 indicating this is a color
    elif isinstance(cmap, tuple) and len(cmap) == 3:
        red, green, blue = cmap
        color_array.red[:] = red
        color_array.green[:] = green
        color_array.blue[:] = blue

    # Otherwise, assume it is a string naming a Matplotlib cmap
    else:
        from matplotlib.pyplot import get_cmap
        cmap = get_cmap(cmap, length)
        for n in range(length):
            r, g, b, _ = cmap(n)
            color_array[n] = _float2int(r, g, b)
    return color_array


def create_burst_coloring():
    offset_c = 30
    colors = create_color_array('strandtest_rainbow', 60)[offset_c: offset_c + 21:5]
    return np.hstack([colors, colors[-2:0:-1]])


def create_rolling_weights(periods=1, desync_red=True, desync_blue=True):
    if periods > 1:
        weights = 1 - (0.5 * np.sin(np.linspace(0, periods * 2 * np.pi, LED_COUNT)) + 0.5)
    else:
        weights = np.linspace(-1, 1, LED_COUNT) ** 2
    weights_rgb = dict()
    weights_rgb['green'] = weights
    weights_rgb['red'] = weights
    weights_rgb['blue'] = weights

    if desync_red:
        weights_rgb['red'] = np.roll(weights, round(LED_COUNT * (1 / 3)))

    if desync_blue:
        weights_rgb['blue'] = np.roll(weights, round(LED_COUNT * (2 / 3)))

    return weights_rgb


def create_color_gradient_array(length, red_start, red_end, green_start, green_end, blue_start, blue_end):
    red = np.linspace(red_start, red_end, length, dtype='int')
    green = np.linspace(green_start, green_end, length, dtype='int')
    blue = np.linspace(blue_start, blue_end, length, dtype='int')
    color_array = create_rgb_array((length,))
    color_array.red = red
    color_array.green = green
    color_array.blue = blue
    return color_array


def _float2int(*args):
    out = list()
    for arg in args:
        out.append(int(round(arg * 255)))
    return tuple(out)


def _rainbow(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)
