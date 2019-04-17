import random

import numpy as np

from config import LED_COUNT
from utils import create_color_array, random_color
from base import LEDConfigurationBase, fade_to_frame


class RandomLightsTurningOn(LEDConfigurationBase):
    def __init__(self, shuffle, palettes, random_width, fading_frame, fade_rate, fade_freq, turn_on_freq):
        super().__init__()
        self.palettes = palettes
        self.shuffle = shuffle
        self.random_width = random_width
        self.fading_frame = fading_frame
        self.fade_rate = fade_rate
        self.fade_freq = fade_freq
        self.turn_on_freq = turn_on_freq

        self.idx = 0
        self.fade_colors()
        if isinstance(palettes[0], np.record):
            self.palette = palettes
            self.turn_on_led()
        elif isinstance(palettes[0], np.ndarray):
            self.create_burst()
        else:
            raise Exception

    def create_burst(self):
        palette = self.palettes[self.idx]
        self.idx = (self.idx + 1) % len(self.palettes)

        offset = random.randint(palette.shape[0], LED_COUNT - palette.shape[0])
        self.frame[offset: offset + palette.shape[0]] = palette
        self.draw_frame()
        self.call_later(self.turn_on_freq, self.create_burst)

    def turn_on_led(self):
        if self.shuffle:
            color = random_color(self.palette)
        else:
            color = self.palette[self.idx]
            self.idx = (self.idx + 1) % len(self.palette)

        offset = random.randint(0, LED_COUNT - 1)

        width = random.randint(*self.random_width)

        self.frame[offset: offset + width] = color
        self.draw_frame()

        self.call_later(self.turn_on_freq, self.turn_on_led)

    def fade_colors(self):
        self.frame = fade_to_frame(self.fading_frame, self.frame, self.fade_rate)
        self.draw_frame()
        self.call_later(self.fade_freq, self.fade_colors)


class RollingWeights(LEDConfigurationBase):
    def __init__(self, base_frame, weights, roll_step, roll_freq):
        super().__init__()
        self.base_frame = base_frame
        self.weights = weights
        self.roll_step = roll_step
        self.roll_freq = roll_freq
        self.draw_and_roll()

    def draw_and_roll(self):
        self.frame.red = np.round(self.base_frame.red * self.weights['red'])
        self.frame.green = np.round(self.base_frame.green * self.weights['green'])
        self.frame.blue = np.round(self.base_frame.blue * self.weights['blue'])
        self.draw_frame()

        for chan, val in self.weights.items():
            self.weights[chan] = np.roll(val, self.roll_step)

        self.call_later(self.roll_freq, self.draw_and_roll)


class PulseCycling(LEDConfigurationBase):
    def __init__(self, base_frame, offsets, fading_frame, fade_rate, fade_freq, turn_on_freq):
        super().__init__()
        self.base_frame = base_frame
        self.offsets = offsets
        self.fading_frame = fading_frame
        self.fade_rate = fade_rate
        self.fade_freq = fade_freq
        self.turn_on_freq = turn_on_freq

        self.turn_on_next_led()
        self.fade_colors()

    def turn_on_next_led(self):
        self.offsets = (self.offsets + 1) % LED_COUNT
        self.frame[self.offsets] = self.base_frame[self.offsets]
        self.draw_frame()
        self.call_later(self.turn_on_freq, self.turn_on_next_led)

    def fade_colors(self):
        self.frame = fade_to_frame(self.fading_frame, self.frame, self.fade_rate)
        self.draw_frame()
        self.call_later(self.fade_freq, self.fade_colors)


class TurnOnAll(LEDConfigurationBase):
    def __init__(self, color):
        super().__init__()
        self.frame = create_color_array(color, LED_COUNT)
        print(self.frame)
        self.draw_frame()
