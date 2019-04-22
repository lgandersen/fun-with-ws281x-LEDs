import random

import numpy as np
from utils import create_rgb_array, random_color


def create_colormap_slice(cmap, start, end, length, ratio=10):
    """ Create a subsection having length `length` of a predifined colormap
    `cmap` using relative coordinates `start` and `end`. Coordinates is specified
    as percentages, e.g., `start=50` and `end=75` means start 50% into the colormap
    and stop 75% into the colormap.
    """
    colormap_large = create_colormap(cmap, ratio*length)
    start = round((start/100) * length)
    end = round((end/100) * length)
    return colormap_large[start:end]


def create_random_discrete_colormap(colors, width_mean, width_variance, length):
    palette = create_rgb_array((length,))
    offset = 0
    while offset < length:
        size = round(random.normalvariate(width_mean, width_variance))
        color = random_color(colors)
        palette[offset: offset + size] = color
        offset += size
    palette[offset:] = random_color(colors)
    return palette


def create_striped_colormap(colors, seglen, length):
    """ Create a colormap of length `length` by cycling
    through the colors in `colors` and creating segments
    of length `seglen`.
    """
    idx = 0
    offset = 0
    colormap = create_rgb_array((length,))
    while offset < length:
        color = colors[idx]
        colormap[offset: offset + seglen] = color
        idx += 1
        offset += seglen
    return colormap


def create_discrete_colormap(colors, sizes):
    """ Create a colormap witch blocks of equal color.
    Block *i* is having colors[i] color and sizes[i] length
    """
    length = sum(sizes)
    palette = create_rgb_array((length,))
    offset = 0
    for n, size  in enumerate(sizes):
        palette[offset:offset + size] = colors[n]
        offset += size
    return palette


def create_colormap(cmap, length):
    color_array = create_rgb_array((length,))
    # Pseudo-cmap made from strandtest.py rainbow-function
    if cmap == 'strandtest_rainbow':
        pos = np.linspace(0, 255, length, dtype='int')
        for idx, _ in enumerate(pos):
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


def _float2int(*args):
    out = list()
    for arg in args:
        out.append(int(round(arg * 255)))
    return tuple(out)

def _rainbow(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    pos -= 170
    return (0, pos * 3, 255 - pos * 3)
