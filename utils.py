from matplotlib.pyplot import get_cmap
import numpy as np


def color_array(cmap, length):
    color_array = np.zeros((length, 3), dtype='int')
    if cmap == 'strandtest_rainbow':
        pos = np.linspace(0, 255, length, dtype='int')
        for idx in range(len(pos)):
            color_array[idx, :] = _rainbow(pos[idx])
    else:
        cmap = get_cmap(cmap, length)
        for n in range(length):
            r, g, b, _ = cmap(n)
            color_array[n, :] = float2int(r, g, b)
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
