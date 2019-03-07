import asyncio

import numpy as np

from playbooks import RandomLightsTurningOnAndFading, PulseCycling, ColorBurst
from utils import RGB, create_color_array

def create_burst_coloring():
    offset_c = 30
    colors = create_color_array('strandtest_rainbow', 60)[offset_c: offset_c + 21:2]
    return np.hstack([colors, colors[-2:0:-1]])

if __name__ == '__main__':
    print ('Press Ctrl-C to quit.')
    try:
        config = {
            'shuffle_colors':False,
            'cmap':'strandtest_rainbow',
            'base_color':RGB(r=0, g=0, b=0),
            'fade_rate':0.10,
            'fade_freq':20, # [ms]
            'turn_on_freq':20, #[ms]
            'offsets':[0, 75], # Used by PulseCycling
            'burst_freq':100, # used by ColorBurst
            'burst_coloring':create_burst_coloring()
                }
        #lightcfg = RandomLightsTurningOnAndFading(cmap='strandtest_rainbow', shuffle_colors=True)
        #lightcfg = RandomLightsTurningOnAndFading(cmap='strandtest_rainbow')
        lightcfg = PulseCycling(config)
        #lightcfg = ColorBurst(config)

        # Blocking call interrupted by loop.stop()
        print('running forever now...')
        loop = asyncio.get_event_loop()
        loop.run_forever()
    except KeyboardInterrupt:
        lightcfg.clear()
        loop.close()
