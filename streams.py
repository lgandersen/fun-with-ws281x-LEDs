import random
import itertools

import numpy as np
#from strip import clear_all, set_colors_all

from utils import RGB
from utils import random_color
from colormap import create_colormap
from config import LED_COUNT


class FrameStreamBase:
    parameters = None
    frame = create_colormap(RGB(r=0, g=0, b=0), LED_COUNT)

    def __init__(self, **kwargs):
        for parameter in self.parameters:
            try:
                setattr(self, parameter, kwargs[parameter])
            except:
                raise Exception("Parameter '{}' was not provided.".format(parameter))


def morph_frame(base_frame, frame2morph, fade_rate):
    red, green, blue = base_frame.red, base_frame.green, base_frame.blue

    frame2morph.red = frame2morph.red + (red - frame2morph.red) * fade_rate
    frame2morph.green = frame2morph.green + (green - frame2morph.green) * fade_rate
    frame2morph.blue = frame2morph.blue + (blue - frame2morph.blue) * fade_rate
    return frame2morph


class PulseCycling(FrameStreamBase):
    parameters = (
        'base_frame',
        'offsets',
        'fading_frame',
        'fade_rate',
        'turn_on_freq',
        'turn_on_at_once',
        )

    def __iter__(self):
        for n in itertools.count():
            if ((n + 1) % self.turn_on_freq) == 0:
                self.move_pulses()

            self.fade_colors()
            yield self.frame

    def move_pulses(self):
        for _ in range(self.turn_on_at_once):
            self.offsets = (self.offsets + 1) % LED_COUNT
            self.frame[self.offsets] = self.base_frame[self.offsets]

    def fade_colors(self):
        self.frame = morph_frame(self.fading_frame, self.frame, self.fade_rate)


class RollingPalette(FrameStreamBase):
    parameters = (
        'rolling_palette',
        'roll_step',
        'roll_freq'
        )

    def __iter__(self):
        for n in itertools.count():
            if (n % self.roll_freq) == 0:
                self.roll()

            yield self.frame


    def roll(self):
        self.rolling_palette = np.roll(self.rolling_palette, self.roll_step)
        self.frame[:] = self.rolling_palette[:LED_COUNT]


class RollingWeights(FrameStreamBase):
    parameters = (
        'base_frame',
        'weights',
        'roll_step',
        'roll_freq'
        )

    def __iter__(self):
        for n in itertools.count():
            if (n % self.roll_freq) == 0:
                self.roll()

            yield self.frame

    def roll(self):
        self.frame.red = np.round(self.base_frame.red * self.weights['red'])
        self.frame.green = np.round(self.base_frame.green * self.weights['green'])
        self.frame.blue = np.round(self.base_frame.blue * self.weights['blue'])

        for chan, val in self.weights.items():
            self.weights[chan] = np.roll(val, self.roll_step)


class RandomLightsTurningOn(FrameStreamBase):
    parameters = (
        'palette',
        'shuffle',
        'random_width',
        'fading_frame',
        'fade_rate',
        'turn_on_freq'
        )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.idx = 0

    def __iter__(self):
        for n in itertools.count():
            yield self.frame
            if ((n + 1) % self.turn_on_freq) == 0:
                self.turn_on_led()

            self.fade_colors()


    def turn_on_led(self):
        if self.shuffle:
            color = random_color(self.palette)
        else:
            color = self.palette[self.idx]
            self.idx = (self.idx + 1) % len(self.palette)

        offset = random.randint(0, LED_COUNT - 1)
        width = random.randint(*self.random_width)
        self.frame[offset: offset + width] = color

    def fade_colors(self):
        self.frame = morph_frame(self.fading_frame, self.frame, self.fade_rate)


class TurnOnAll(FrameStreamBase):
    parameters = ('color')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frame = create_colormap(self.color, LED_COUNT)

    def __iter__(self):
        while True:
            yield self.frame
