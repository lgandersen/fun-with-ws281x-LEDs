import random

from config import LED_COUNT
from utils import create_color_array, random_led, random_color
from base import LEDConfigurationBase


class RandomLightsTurningOnAndFading(LEDConfigurationBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.colors = create_color_array(self.cmap, LED_COUNT)
        self.set_color_all(self.base_color)
        self.call_later(self.fade_freq, self.converge_to_basecolor, self.base_color, self.fade_rate)
        self.call_later(self.turn_on_freq, self.turn_on_led)

    def turn_on_led(self):
        idx = random_led()
        if self.shuffle_colors:
            color = random_color(self.colors)
        else:
            color = self.colors[idx]
        self.set_color(idx, color)
        self.render()
        self.call_later(self.turn_on_freq, self.turn_on_led)


class PulseCycling(LEDConfigurationBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.colors = create_color_array(self.cmap, LED_COUNT)
        self.call_later(self.fade_freq, self.converge_to_basecolor, self.base_color, self.fade_rate)
        self.call_later(self.turn_on_freq, self.turn_on_next_led)

    def turn_on_next_led(self):
        for n, idx in enumerate(self.offsets):
            self.set_color(idx, self.colors[idx])
            self.offsets[n] = (idx + 1) % LED_COUNT
        self.render()
        self.call_later(self.turn_on_freq, self.turn_on_next_led)


class ColorBurst(LEDConfigurationBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.set_color_all(self.base_color)
        self.create_burst()
        self.call_later(self.fade_freq, self.converge_to_basecolor, self.base_color, self.fade_rate)

    def create_burst(self):
        self.offset = random.randint(self.burst_coloring.shape[0], LED_COUNT - self.burst_coloring.shape[0])
        count = 0
        for idx in range(self.offset, self.offset + self.burst_coloring.shape[0]):
            self.set_color(idx, self.burst_coloring[count])
            count += 1
        self.render()
        self.call_later(self.burst_freq, self.create_burst)
