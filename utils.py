import random
from matplotlib.pyplot import get_cmap
import numpy as np
from config import LED_COUNT


def random_led():
    return random.randint(0, LED_COUNT - 1)


def random_color(colors):
    idx = random.randint(0, colors.shape[0] - 1)
    return colors[idx]


def color_array(cmap, length):
    color_array = create_rgb_array((length,)) #np.zeros((length, 3), dtype=rgb_type)
    if cmap == 'strandtest_rainbow':
        pos = np.linspace(0, 255, length, dtype='int')
        for idx in range(len(pos)):
            color_array[idx] = _rainbow(pos[idx])
    else:
        cmap = get_cmap(cmap, length)
        for n in range(length):
            r, g, b, _ = cmap(n)
            color_array[n] = float2int(r, g, b)
    return color_array


def float2int(*args):
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


rgb_type = np.dtype([('red', 'uint32'), ('green', 'uint32'), ('blue', 'uint32')])

def create_rgb_array(shape):
    if isinstance(shape, int):
        array = np.zeros((shape,), dtype=rgb_type)
    else:
        array = np.zeros(shape, dtype=rgb_type)
    return array.view(np.recarray)
