import numpy as np

from playbooks import RollingPalette, RandomLightsTurningOn, PulseCycling, \
        RollingWeights
from player import Player, iter_random_lights_turning_on_configs, iter_pulse_cycling_configs
from config import LED_COUNT
from strip import clear_all
from utils import create_rolling_weights, RGB
from colormap import create_colormap, create_random_discrete_colormap, create_colormap_slice

workbooks = [
    (RandomLightsTurningOn, {
        'shuffle':True,
        'palettes':create_colormap('strandtest_rainbow', LED_COUNT),
        'random_width':(5, 10), # Tuple (start, end) of random sampled widths (start == end implies fixed width)
        'fading_frame':create_colormap(RGB(r=0, g=0, b=0), LED_COUNT),
        'fade_rate':0.50,
        'fade_freq':10, # [ms]
        'turn_on_freq':0, #[ms]
        }),
    (RandomLightsTurningOn, {
        'shuffle':False,
        'palettes':[create_colormap_slice('strandtest_rainbow', start=50, end=75, length=25, ratio=1)],
        'random_width':(1, 1), # Tuple (start, end) of random sampled widths (start == end implies fixed width)
        'fading_frame':create_colormap(RGB(r=0, g=0, b=0), LED_COUNT),
        'fade_rate':0.05,
        'fade_freq':10, # [ms]
        'turn_on_freq':0, #[ms]
        }),
    (RollingWeights, {
        'base_frame':create_colormap('prism', LED_COUNT),
        'weights':create_rolling_weights(periods=5, desync_blue=False, desync_red=True), # Array to use for rolling
        'roll_step':1, # Size of increment in array a each array-roll
        'roll_freq':0, # Update frequency of the rolling array
        }),
    (PulseCycling, {
        'base_frame':create_colormap('strandtest_rainbow', LED_COUNT),
        'offsets':np.arange(0, LED_COUNT, 25), # offsets (and number) of pulses
        'fading_frame':create_colormap(RGB(r=0, g=0, b=0), LED_COUNT),
        'fade_rate':0.50,
        'fade_freq':10, # [ms]
        'turn_on_freq':0, #[ms]
        'turn_on_at_once':1,
        }),
    (RollingPalette, {
        'roll_step':3,
        'roll_freq':0,
        'rolling_palette':create_random_discrete_colormap(
            create_colormap('strandtest_rainbow', 20), 10, 10, LED_COUNT),
        })
    ]

if __name__ == '__main__':
    #workbooks = [workbooks[0]] #While debugging
    #workbooks = [(PulseCycling, cfg) for cfg in iter_pulse_cycling_configs(20)]
    workbooks = [(RandomLightsTurningOn, cfg) for cfg in iter_random_lights_turning_on_configs(20)]
    print('Press Ctrl-C to quit.')
    try:
        cwbs = Player(workbooks)
        cwbs.start()
    except KeyboardInterrupt:
        cwbs.loop.close()
        clear_all()
