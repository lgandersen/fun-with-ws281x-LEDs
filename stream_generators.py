from random import randint

import numpy as np
from numpy.random import choice as choose

from config import LED_COUNT
from utils import RGB
from colormap import create_colormap
from streams import PulseCycling, RandomLightsTurningOn


def _choose_cmap_frame(frames_cmap):
    return frames_cmap[choose(len(frames_cmap))]


def _no_lights_or_random_cmap(frames_cmap, likelihood=2):
    if randint(0, likelihood) == 0:
        cmap = create_colormap(RGB(r=0, g=0, b=0), LED_COUNT)
    else:
        cmap = frames_cmap[choose(len(frames_cmap))]
    return cmap


def all_streams(limit):
    for stream1, stream2 in zip(
            random_lights_turning_streams(limit),
            pulse_cycling_streams(limit)
            ):
        yield stream1
        yield stream2


def random_lights_turning_streams(limit=99999):
    frames_cmap = [
        create_colormap('strandtest_rainbow', LED_COUNT),
        #create_colormap('prism', LED_COUNT),
        #create_colormap('jet', LED_COUNT),
    ]
    random_widths = [
        (2, 2),
        (1, 5),
        (5, 10),
        (5, 25)
        ]
    count = 0
    while count < limit:
        cfg = {
            'shuffle':choose([True, False]),
            'palette':_choose_cmap_frame(frames_cmap),
            # Tuple (start, end) of random sampled widths (start == end implies fixed width):
            'random_width':random_widths[choose(len(random_widths))],
            'fading_frame':create_colormap(RGB(r=0, g=0, b=0), LED_COUNT),
            'fade_rate':choose([0, 0.005, 0.01, 0.10]),
            'turn_on_freq':choose([0, 0, 5, 10]),
            }
        yield RandomLightsTurningOn(**cfg)
        count += 1


def pulse_cycling_streams(limit=999999):
    frames_cmap = [
        create_colormap('strandtest_rainbow', LED_COUNT),
        #create_colormap('prism', LED_COUNT),
        #create_colormap('jet', LED_COUNT),
        ] + [
        create_colormap(tuple(color), LED_COUNT)
        for n, color in enumerate(create_colormap('strandtest_rainbow', 20))
        if n % 4 == 0
        ]
    count = 0
    while count < limit:
        cfg = {
            #'fading_frame':_no_lights_or_random_cmap(frames_cmap),
            'fading_frame':create_colormap(RGB(r=0, g=0, b=0), LED_COUNT),
            'base_frame':frames_cmap[choose(len(frames_cmap))],
            'offsets':np.arange(0, LED_COUNT, choose([25, 40, 50])),
            'fade_rate':choose([0.05, 0.10, 0.20]),
            'turn_on_freq':choose([0, 0, 5, 10]),
            'turn_on_at_once':choose([1, 1, 2]),
            }
        yield PulseCycling(**cfg)
        count += 1
