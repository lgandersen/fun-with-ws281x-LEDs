import numpy as np

from streams import TurnOnAll, PulseCycling, RollingPalette, RollingWeights, RandomLightsTurningOn, MonteCarloColoring
from player import LEDPlayer
from stream_generators import all_streams#, random_lights_turning_streams, pulse_cycling_streams
from config import LED_COUNT
from strip import clear_all
from utils import create_oscilating_weights, RGB
from colormap import create_colormap#, create_random_discrete_colormap, create_colormap_slice


streams = [
    RandomLightsTurningOn(**{
        'shuffle':True,
        'palette':create_colormap('strandtest_rainbow', LED_COUNT),
        'random_width':(10, 20), # Tuple (start, end) of random sampled widths (start == end implies fixed width)
        'fading_frame':create_colormap(RGB(r=0, g=0, b=0), LED_COUNT),
        'fade_rate':0.05,
        'turn_on_freq':5, # Turn on every <turn_on_freq>th frame
        }),
    RollingWeights(**{
        'base_frame':create_colormap('prism', LED_COUNT),
        #'base_frame':create_colormap('strandtest_rainbow', LED_COUNT),
        'weights':create_oscilating_weights(periods=5, desync_blue=True, desync_red=True), # Array to use for rolling
        'roll_step':1, # Size of increment in array a each array-roll
        'roll_freq':1, # Update frequency of the rolling array
        }),
    PulseCycling(**{
        'base_frame':create_colormap('strandtest_rainbow', LED_COUNT),
        #'offsets':np.arange(0, LED_COUNT, 25), # offsets (and number) of pulses
        'offsets':np.arange(0, LED_COUNT, 15), # offsets (and number) of pulses
        'fading_frame':create_colormap(RGB(r=0, g=0, b=0), LED_COUNT),
        'fade_rate':0.10,
        'turn_on_freq':1, #[ms]
        'turn_on_at_once':1,
        }),
    RollingPalette(**{
        'roll_step':3,
        'roll_freq':5,
        'rolling_palette': create_colormap('strandtest_rainbow', LED_COUNT)
        #'rolling_palette': create_random_discrete_colormap(
        #    create_colormap('strandtest_rainbow', 20), 10, 10, LED_COUNT),
        }),
    MonteCarloColoring(**{
        'nsources':4,
        'turn_on_freq':1
        })
    ]

turn_off = [(TurnOnAll, {'color':RGB(r=0, g=0, b=0)})]
turn_on = [TurnOnAll(**{'color':RGB(r=255, g=255, b=255)})]

if __name__ == '__main__':
    print('Press Ctrl-C to quit.')
    try:
        #player = LEDPlayer(turn_on)
        #player = LEDPlayer(streams)
        #player = LEDPlayer([streams[-3:-1]])
        #player = LEDPlayer(streams[-2:])

        player = LEDPlayer([stream for stream in all_streams(500)])
        player.start()
    except KeyboardInterrupt:
        clear_all()
