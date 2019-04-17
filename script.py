import asyncio

import numpy as np

from playbooks import RandomLightsTurningOn, PulseCycling, RollingWeights, TurnOnAll
from utils import create_color_array, sleep_ms
from config import LED_COUNT

from utils import create_burst_coloring, create_rolling_weights, RGB

random_lights_turning_on = {
        'shuffle':True,
        'palettes':create_color_array('strandtest_rainbow', LED_COUNT),
        'random_width':(5, 10), # Tuple (start, end) of random sampled widths (start == end implies fixed width)
        'fading_frame':create_color_array(RGB(r=0, g=0, b=0), LED_COUNT),
        'fade_rate':0.50,
        'fade_freq':10, # [ms]
        'turn_on_freq':0, #[ms]
        }

color_burst = {
        'shuffle':False,
        'palettes':[create_burst_coloring()],
        'random_width':(1, 1), # Tuple (start, end) of random sampled widths (start == end implies fixed width)
        'fading_frame':create_color_array(RGB(r=0, g=0, b=0), LED_COUNT),
        'fade_rate':0.50,
        'fade_freq':10, # [ms]
        'turn_on_freq':0, #[ms]
        }


rolling_weights = {
        'base_frame':create_color_array('prism', LED_COUNT),
        'weights':create_rolling_weights(periods=5, desync_blue=True, desync_red=True), # Array to use for rolling
        'roll_step':1, # Size of increment in array a each array-roll
        'roll_freq':1, # Update frequency of the rolling array
        }


pulsating_lights = {
        'base_frame':create_color_array('strandtest_rainbow', LED_COUNT),
        'offsets':np.arange(0, LED_COUNT, 25), # offsets (and number) of pulses
        'fading_frame':create_color_array(RGB(r=0, g=0, b=0), LED_COUNT),
        'fade_rate':0.50,
        'fade_freq':10, # [ms]
        'turn_on_freq':0, #[ms]
        }

turn_on_all = {
        'color':(0, 0, 255)
        }


class CycleWorkbooks:
    def __init__(self):
        self.switch_rate = 30
        self.workbooks = [
                (PulseCycling, pulsating_lights),
                (RandomLightsTurningOn, color_burst),
                (RandomLightsTurningOn, random_lights_turning_on),
                (RollingWeights, rolling_weights),
                (TurnOnAll, turn_on_all)
                ]
        #self.workbooks = [self.workbooks[0]] #While debugging
        self.workbook_idx = 0
        self.present_workbook = None
        self.loop = asyncio.get_event_loop()

    def start(self):
        self.change_workbook()
        self.loop.run_forever()

    def change_workbook(self):
        if self.present_workbook is not None:
            self.present_workbook.stop()
            sleep_ms(2000)
        print('Changing to workbook ', self.workbook_idx, self.workbooks[self.workbook_idx][0])
        workbook, cfg = self.workbooks[self.workbook_idx]
        self.present_workbook = workbook(**cfg)
        self.workbook_idx = (self.workbook_idx + 1) % len(self.workbooks)
        self.loop.call_later(self.switch_rate, self.change_workbook)


if __name__ == '__main__':
    print ('Press Ctrl-C to quit.')
    try:
        cwbs = CycleWorkbooks()
        cwbs.start()

        # Blocking call interrupted by loop.stop()
        print('running forever now...')
    except KeyboardInterrupt:
        cwbs.loop.close()
