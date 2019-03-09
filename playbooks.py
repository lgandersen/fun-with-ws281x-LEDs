import random

import numpy as np

from config import LED_COUNT
from utils import create_color_array, random_led, random_color
from base import LEDConfigurationBase


class RandomLightsTurningOnAndFading(LEDConfigurationBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.colors = create_color_array(self.cmap, LED_COUNT)
        self.set_color_all(self.base_color)
        self.turn_on_led()
        self.fade_to_basecolor(self.base_color, self.fade_rate)

    def turn_on_led(self):
        if self.random_width is not None:
            width = random.randint(1, 5)
        else:
            width = self.pixel_width

        idx = random_led()
        if self.shuffle_colors:
            color = random_color(self.colors)
        else:
            color = self.colors[idx]
        for n in range(idx, idx + width):
            if n < LED_COUNT:
                self.set_color(n, color)
        self.render()
        self.call_later(self.turn_on_freq, self.turn_on_led)


class RollColoring(LEDConfigurationBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.draw_and_roll()

    def draw_and_roll(self):
        for n in range(LED_COUNT - 1):
            self.set_color(n, self.rolling_colors[n])
        self.render()
        self.rolling_colors = np.roll(self.rolling_colors, self.roll_step)
        self.call_later(self.roll_freq, self.draw_and_roll)


class PulseCycling(LEDConfigurationBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.colors = create_color_array(self.cmap, LED_COUNT)
        self.call_later(self.fade_freq, self.fade_to_basecolor, self.base_color, self.fade_rate)
        self.call_later(self.turn_on_freq, self.turn_on_next_led)

    def turn_on_next_led(self):
        for n, idx in enumerate(self.offsets):
            self.set_color(idx, self.colors[idx])
            self.offsets[n] = (idx + 1) % LED_COUNT
        self.render()
        self.call_later(self.turn_on_freq, self.turn_on_next_led)


class ColorBursts(LEDConfigurationBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.set_color_all(self.base_color)
        self.create_burst()
        self.call_later(self.fade_freq, self.fade_to_basecolor, self.base_color, self.fade_rate)

    def create_burst(self):
        self.offset = random.randint(self.burst_coloring.shape[0], LED_COUNT - self.burst_coloring.shape[0])
        count = 0
        for idx in range(self.offset, self.offset + self.burst_coloring.shape[0]):
            self.set_color(idx, self.burst_coloring[count])
            count += 1
        self.render()
        self.call_later(self.burst_freq, self.create_burst)
