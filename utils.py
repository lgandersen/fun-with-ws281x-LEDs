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


def random_color(colormap):
    idx = random.randint(0, colormap.shape[0] - 1)
    return colormap[idx]


## FIXME Need to makes this awesome!
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
