import asyncio

import numpy as np

from playbooks import RandomLightsTurningOnAndFading, PulseCycling, ColorBursts, RollColoring
from utils import RGB, create_color_array, LED_COUNT, sleep_ms

def create_burst_coloring():
    offset_c = 30
    colors = create_color_array('strandtest_rainbow', 60)[offset_c: offset_c + 21:5]
    return np.hstack([colors, colors[-2:0:-1]])


def create_rolling_array():
    colors = create_color_array(RGB(r=0, g=250, b=0), LED_COUNT)
    #periods = 1
    #weights = (0.5 * np.sin(np.linspace(0, periods * 2 * np.pi, LED_COUNT)) + 0.5) ** 2
    #weights = 0.5 * np.sin(np.linspace(0, periods * 2 * np.pi, LED_COUNT)) + 0.5
    #weights = 0.95 * self.weights + 0.05
    #weights = np.abs(np.linspace(-1, 1, LED_COUNT))
    #weights[self.weights < 0.1] = 0
    weights = (np.linspace(-1, 1, LED_COUNT) ** 2) #* 0.99 + 0.01
    #colors.red = 255 - np.round(colors.green * self.weights)
    colors.red = np.round(colors.red * weights)
    colors.green = np.round(colors.green * weights)
    colors.blue = np.round(colors.blue * weights)
    return colors

class CycleWorkbooks:
    def __init__(self, config):
        self.switch_rate = 60
        self.workbooks = [
                PulseCycling,
                ColorBursts,
                RandomLightsTurningOnAndFading,
                RollColoring,
                ]
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
            'cmap':'strandtest_rainbow',
            'base_color':RGB(r=0, g=0, b=0),
            'fade_rate':0.10,
            'fade_freq':20, # [ms]
            'turn_on_freq':10, #[ms]
            'offsets':[0, 50, 100], # Used by PulseCycling

            # ColorBursts only
            'burst_freq':1000,                         # Frequency of creating new bursts
            'burst_coloring':create_burst_coloring(), # Burst coloring array

            # RandomLightsTurningOnAndFading only
            'random_width':(1, 5), # Used by RandomLightsTurningOnAndFading. Can be a range (start, end) of possible widths
            'pixel_width':1,     # Used by RandomLightsTurningOnAndFading. Denotes the width of LEDs that is turned on at random. If 'random_width' i set this is not used.

            # RollColoring only
            'rolling_colors':create_rolling_array(), # Array to use for rolling
            'roll_freq':1,                           # Update frequency of the rolling array
            'roll_step':1,                           # Size of increment in array a each array-roll
                }
        cwbs = CycleWorkbooks(config)
        cwbs.start()

        # Blocking call interrupted by loop.stop()
        print('running forever now...')
    except KeyboardInterrupt:
        cwbs.present_workbook.clear()
        cwbs.loop.close()
