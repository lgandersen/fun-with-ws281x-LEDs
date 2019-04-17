import asyncio

import numpy as np

from playbooks import RandomLightsTurningOnAndFading, PulseCycling, ColorBursts, RollColoring, TurnOnAllOnce
from utils import RGB, create_color_array, LED_COUNT, sleep_ms

def create_burst_coloring():
    offset_c = 30
    colors = create_color_array('strandtest_rainbow', 60)[offset_c: offset_c + 21:5]
    return np.hstack([colors, colors[-2:0:-1]])


def create_rolling_weights(periods=1, desync_red=True, desync_blue=True):
    if periods > 1:
        weights = 1 - (0.5 * np.sin(np.linspace(0, periods * 2 * np.pi, LED_COUNT)) + 0.5)
    else:
        weights = np.linspace(-1, 1, LED_COUNT) ** 2
    weights_rgb = dict()
    weights_rgb['green'] = weights
    weights_rgb['red'] = weights
    weights_rgb['blue'] = weights

    if desync_red:
        weights_rgb['red'] = np.roll(weights, round(LED_COUNT * (1 / 3)))

    if desync_blue:
        weights_rgb['blue'] = np.roll(weights, round(LED_COUNT * (2 / 3)))

    return weights_rgb

class CycleWorkbooks:
    def __init__(self, config):
        self.switch_rate = 90
        self.workbooks = [
                PulseCycling,
                ColorBursts,
                RandomLightsTurningOnAndFading,
                RollColoring,
                TurnOnAllOnce
                ]
        self.workbooks = [self.workbooks[0]] #While debugging
        self.config = config
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
        print('Changing to workbook ', self.workbook_idx, self.workbooks[self.workbook_idx])
        self.present_workbook = self.workbooks[self.workbook_idx](self.config)
        self.workbook_idx = (self.workbook_idx + 1) % len(self.workbooks)
        self.loop.call_later(self.switch_rate, self.change_workbook)


if __name__ == '__main__':
    print ('Press Ctrl-C to quit.')
    try:
        config = {
            'shuffle_colors':True,
            #'cmap':'strandtest_rainbow',
            'cmap':'prism',
            'base_color':create_color_array(RGB(r=0, g=0, b=0), LED_COUNT),
            'fade_rate':0.10,
            'fade_freq':10, # [ms]
            'turn_on_freq':0, #[ms]
            'offsets':[0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 420, 450], # Used by PulseCycling

            # ColorBursts only
            'burst_freq':1000,                         # Frequency of creating new bursts
            'burst_coloring':create_burst_coloring(), # Burst coloring array

            # RandomLightsTurningOnAndFading only
            'random_width':(10, 15), # Used by RandomLightsTurningOnAndFading. Can be a range (start, end) of possible widths
            'pixel_width':1,     # Used by RandomLightsTurningOnAndFading. Denotes the width of LEDs that is turned on at random. If 'random_width' i set this is not used.

            # RollColoring only
            #'roll_base_color':create_color_array('strandtest_rainbow', LED_COUNT),
            'roll_base_color':create_color_array('prism', LED_COUNT),
            'rolling_weights':create_rolling_weights(periods=5, desync_blue=True, desync_red=True), # Array to use for rolling
            'roll_freq':1,                           # Update frequency of the rolling array
            'roll_step':1,                           # Size of increment in array a each array-roll
                }
        cwbs = CycleWorkbooks(config)
        cwbs.start()

        # Blocking call interrupted by loop.stop()
        print('running forever now...')
    except KeyboardInterrupt:
        cwbs.loop.close()
