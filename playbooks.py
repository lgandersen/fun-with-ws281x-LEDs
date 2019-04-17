import random

import numpy as np

from config import LED_COUNT
from utils import create_color_array, random_led, random_color, create_rgb_array
from base import LEDConfigurationBase, fade_to_base_coloring
from strip import set_colors_all, set_colors


class RandomLightsTurningOnAndFading(LEDConfigurationBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.palette = create_color_array(self.cmap, LED_COUNT)
        self.coloring = self.base_color.copy()
        set_colors_all(self.base_color)
        self.turn_on_led()
        self.fade_colors()

    def turn_on_led(self):
        if self.random_width is not None:
            width = random.randint(1, 5)
        else:
            width = self.pixel_width

        idx = random_led()
        if self.shuffle_colors:
            color = random_color(self.palette)
        else:
            color = self.palette[idx]


        color_spot = create_color_array((color.red, color.green, color.blue), width)
        idx = np.arange(idx, idx + width)
        self.coloring[idx] = color_spot

        set_colors(idx, color_spot)
        self.call_later(self.turn_on_freq, self.turn_on_led)

    def fade_colors(self):
        self.coloring = fade_to_base_coloring(self.base_color, self.coloring, self.fade_rate)
        set_colors_all(self.coloring)
        self.call_later(self.fade_freq, self.fade_colors)


class RollColoring(LEDConfigurationBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.draw_and_roll()

    def draw_and_roll(self):
        colors = self.roll_base_color.copy()
        weights = self.rolling_weights
        colors.red = np.round(colors.red * weights['red'])
        colors.green = np.round(colors.green * weights['green'])
        colors.blue = np.round(colors.blue * weights['blue'])
        set_colors_all(colors)

        for chan, val in weights.items():
            self.rolling_weights[chan] = np.roll(val, self.roll_step)

        self.call_later(self.roll_freq, self.draw_and_roll)


class PulseCycling(LEDConfigurationBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.offsets = np.array(self.offsets, dtype='int')
        self.pulse_colors = create_color_array(self.cmap, LED_COUNT)
        self.coloring = create_rgb_array((LED_COUNT, ))
        self.call_later(self.fade_freq, self.fade_colors)
        self.call_later(self.turn_on_freq, self.turn_on_next_led)

    def turn_on_next_led(self):
        self.offsets = (self.offsets + 1) % LED_COUNT
        self.coloring[self.offsets] = self.pulse_colors[self.offsets]
        set_colors(self.offsets, self.pulse_colors[self.offsets])
        self.call_later(self.turn_on_freq, self.turn_on_next_led)

    def fade_colors(self):
        self.coloring = fade_to_base_coloring(self.base_color, self.coloring, self.fade_rate)
        set_colors_all(self.coloring)
        self.call_later(self.fade_freq, self.fade_colors)


class ColorBursts(LEDConfigurationBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.coloring = self.base_color.copy()
        set_colors_all(self.coloring)
        self.create_burst()
        self.call_later(self.fade_freq, self.fade_colors)

    def create_burst(self):
        self.offset = random.randint(self.burst_coloring.shape[0], LED_COUNT - self.burst_coloring.shape[0])
        self.coloring[self.offset: self.offset + self.burst_coloring.shape[0]] = self.burst_coloring
        set_colors_all(self.coloring)
        self.call_later(self.burst_freq, self.create_burst)

    def fade_colors(self):
        self.coloring = fade_to_base_coloring(self.base_color, self.coloring, self.fade_rate)
        set_colors_all(self.coloring)
        self.call_later(self.fade_freq, self.fade_colors)


class TurnOnAllOnce(LEDConfigurationBase):
    def __init__(self, *args):
        super().__init__(*args)
        colors = create_color_array((0, 0, 255), LED_COUNT)
        set_colors_all(colors)
