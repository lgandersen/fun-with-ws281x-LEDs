import random

import numpy as np

from config import LED_COUNT
from utils import create_color_array, random_color
from base import LEDConfigurationBase, morph_frame


class RandomLightsTurningOn(LEDConfigurationBase):
    parameters = (
            'shuffle',
            'palettes',
            'random_width',
            'fading_frame',
            'fade_rate',
            'turn_on_freq'
            )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.idx = 0
        if isinstance(self.palettes[0], np.record):
            self.palette = self.palettes
            self.create_task(self.turn_on_led)
        elif isinstance(self.palettes[0], np.ndarray):
            self.create_task(self.create_burst)
        else:
            raise Exception
        self.create_task(self.fade_colors)

    async def create_burst(self):
        palette = self.palettes[self.idx]
        self.idx = (self.idx + 1) % len(self.palettes)

        offset = random.randint(palette.shape[0], LED_COUNT - palette.shape[0])
        self.frame[offset: offset + palette.shape[0]] = palette

        await self.sleep(self.turn_on_freq)
        self.create_task(self.create_burst)

    async def turn_on_led(self):
        if self.shuffle:
            color = random_color(self.palette)
        else:
            color = self.palette[self.idx]
            self.idx = (self.idx + 1) % len(self.palette)

        offset = random.randint(0, LED_COUNT - 1)
        width = random.randint(*self.random_width)
        self.frame[offset: offset + width] = color

        await self.sleep(self.turn_on_freq)
        self.create_task(self.turn_on_led)

    async def fade_colors(self):
        self.frame = morph_frame(self.fading_frame, self.frame, self.fade_rate)
        self.create_task(self.fade_colors)


class RollingWeights(LEDConfigurationBase):
    parameters = (
            'base_frame',
            'weights',
            'roll_step',
            'roll_freq'
            )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_task(self.draw_and_roll)

    async def draw_and_roll(self):
        self.frame.red = np.round(self.base_frame.red * self.weights['red'])
        self.frame.green = np.round(self.base_frame.green * self.weights['green'])
        self.frame.blue = np.round(self.base_frame.blue * self.weights['blue'])

        for chan, val in self.weights.items():
            self.weights[chan] = np.roll(val, self.roll_step)

        await self.sleep(self.roll_freq)
        self.create_task(self.draw_and_roll)


class PulseCycling(LEDConfigurationBase):
    parameters = (
            'base_frame',
            'offsets',
            'fading_frame',
            'fade_rate',
            'turn_on_freq'
            )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_task(self.turn_on_next_led)
        self.create_task(self.fade_colors)

    async def turn_on_next_led(self):
        self.offsets = (self.offsets + 1) % LED_COUNT
        self.frame[self.offsets] = self.base_frame[self.offsets]
        await self.sleep(self.turn_on_freq)
        self.create_task(self.turn_on_next_led)

    async def fade_colors(self):
        self.frame = morph_frame(self.fading_frame, self.frame, self.fade_rate)
        self.create_task(self.fade_colors)


class TurnOnAll(LEDConfigurationBase):
    parameters = ('color')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frame = create_color_array(self.color, LED_COUNT)
        self.draw_frame()
