import random
import asyncio
import numpy as np

from config import LED_COUNT
from utils import create_color_array, random_led, random_color
from base import LEDConfigurationBase

class RandomLightsTurningOnAndFading(LEDConfigurationBase):
    def __init__(self, cmap='strandtest_rainbow', shuffle_colors=False):
        super().__init__()
        self.base_color = (0, 0 ,0)
        self.fade_rate = 0.10
        self.decrease_frequency = 50 # ms
        self.turn_on_led_every = 200 # ms
        self.colors = create_color_array(cmap, LED_COUNT)
        self.shuffle_colors = shuffle_colors
        self.set_color_all(self.strip, self.color)
        self.call_later(self.decrease_frequency, self.converge_to_basecolor, self.base_color, self.fade_rate)
        self.call_later(self.turn_on_led_every, self.turn_on_led)

    def turn_on_led(self):
        idx = random_led()
        if self.shuffle_colors:
            color = random_color(self.colors)
        else:
            color = self.colors[idx]
        self.set_color(idx, color)
        self.render()
        self.call_later(self.turn_on_led_every, self.turn_on_led)


class PulseCycling(LEDConfigurationBase):
    def __init__(self, cmap='strandtest_rainbow'):
        super().__init__()
        self.base_color = (0, 0 ,0)
        self.fade_rate = 0.10
        self.turn_on_frequency = 30
        self.decrease_frequency = 100
        self.colors = create_color_array(cmap, LED_COUNT)
        self.idx = 0
        self.call_later(self.decrease_frequency, self.converge_to_basecolor, self.base_color, self.fade_rate)
        self.call_later(self.turn_on_frequency, self.turn_on_next_led)

    def turn_on_next_led(self):
        self.set_color(self.idx, self.colors[self.idx])
        self.idx = (self.idx + 1) % LED_COUNT
        self.render()
        self.call_later(self.turn_on_frequency, self.turn_on_next_led)


class ColorBurst(LEDConfigurationBase):
    def __init__(self):
        super().__init__()
        self.create_frequency = 1000
        self.fade_rate = 0.10
        self.decrease_frequency = 100
        offset_c = 0
        self._colors = create_color_array('strandtest_rainbow', 60)[offset_c: offset_c + 21:4]
        self._create_burst_coloring()
        self.set_base_color()
        self.create_burst()
        self.call_later(self.decrease_frequency, self.converge_to_basecolor, self.base_color, self.fade_rate)

    def _create_burst_coloring(self):
        colors = self._colors[1:]
        self.burst_coloring = np.hstack([colors, colors[-2:0:-1]])

    @property
    def base_color(self):
        return self._colors[0]

    @property
    def peak_color(self):
        return self._colors[-1]

    def set_base_color(self):
        for n in range(LED_COUNT - 1):
            self.set_color(n, self.base_color)
        self.render()

    def create_burst(self):
        self.offset = random.randint(self.burst_coloring.shape[0], LED_COUNT - self.burst_coloring.shape[0])
        count = 0
        for idx in range(self.offset, self.offset + self.burst_coloring.shape[0]):
            self.set_color(idx, self.burst_coloring[count])
            count += 1
        self.render()
        self.call_later(self.create_frequency, self.create_burst)


if __name__ == '__main__':
    print ('Press Ctrl-C to quit.')
    try:
        #lightcfg = RandomLightsTurningOnAndFading(cmap='strandtest_rainbow')
        lightcfg = PulseCycling(cmap='strandtest_rainbow')
        #lightcfg = ColorBurst()#cmap='strandtest_rainbow')

        # Blocking call interrupted by loop.stop()
        print('running forever now...')
        loop = asyncio.get_event_loop()
        loop.run_forever()
    except KeyboardInterrupt:
        lightcfg.clear()
        loop.close()
