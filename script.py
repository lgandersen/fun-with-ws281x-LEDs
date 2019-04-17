import numpy as np

from playbooks import RandomLightsTurningOn, PulseCycling, RollingWeights#, TurnOnAll
from player import Player
from utils import create_color_array
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

workbooks = [
    (PulseCycling, pulsating_lights),
    (RandomLightsTurningOn, color_burst),
    (RandomLightsTurningOn, random_lights_turning_on),
    (RollingWeights, rolling_weights),
    #(TurnOnAll, turn_on_all)
    ]

if __name__ == '__main__':
    #workbooks = [workbooks[0]] #While debugging
    from player import iter_pulse_cycling_configs
    workbooks = [(PulseCycling, cfg) for cfg in iter_pulse_cycling_configs(20)]
    print ('Press Ctrl-C to quit.')
    try:
        cwbs = Player(workbooks)
        cwbs.start()

        # Blocking call interrupted by loop.stop()
        print('running forever now...')
    except KeyboardInterrupt:
        cwbs.loop.close()
