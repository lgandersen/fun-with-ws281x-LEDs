import time
import asyncio
import numpy as np
from rpi_ws281x import Adafruit_NeoPixel

from config import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, CORD_LED
from utils import color_array, create_rgb_array, random_led, random_color

def clear(strip):
    """Wipe color across display a pixel at a time."""
    color = color24bit(0, 0, 0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()


def sleep_ms(ms):
    time.sleep(ms/1000.0)


def color24bit(red, green, blue):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    if CORD_LED:
        return int( (green << 16) | (red << 8) | blue )
    else:
        return int( (red << 16) | (green << 8) | blue )


def plot_colormap(strip, cmap):
    print('Plotting colormap: ', cmap)
    colors = color_array(cmap, LED_COUNT)
    print('FARVERNE:', colors)
    for n in range(LED_COUNT - 1):
        color = color24bit(*colors[n,:])
        strip.setPixelColor(n, color)
        strip.show()
    time.sleep(2)

def decrease_brightness(strip, leds, fading_rate=0.90):
    lights_on = (leds.red > 0) | (leds.blue > 0) | (leds.green > 0)
    leds.red = leds.red * fading_rate
    leds.green = leds.green * fading_rate
    leds.blue = leds.blue * fading_rate
    for n in range(leds.size):
        if lights_on[n]:
            color = color24bit(*leds[n])
            strip.setPixelColor(n, color)
    strip.show()


class LightningConfigurationMixin:
    def __init__(self):
        pass

def ms2s(milisecond):
    return milisecond / 1000

class RandomLightsTurningOnAndFading:
    def __init__(self, loop, strip, cmap='strandtest_rainbow', shuffle_colors=False):
        self.decrease_frequency = 50 # ms
        self.turn_on_led_every = 200 # ms
        self.colors = color_array(cmap, LED_COUNT)
        self.strip = strip
        self.leds = create_rgb_array((LED_COUNT,))
        self.loop = loop
        self.shuffle_colors = shuffle_colors
        self.loop.call_later(ms2s(self.decrease_frequency), self.decrease_brightness)
        self.loop.call_later(ms2s(self.turn_on_led_every), self.turn_on_led)

    def turn_on_led(self):
        idx = random_led()
        if self.shuffle_colors:
            color = random_color(self.colors)
        else:
            color = self.colors[idx]
        self.strip.setPixelColor(idx, color24bit(*color))
        self.strip.show()
        self.leds[idx] = color
        self.loop.call_later(ms2s(self.turn_on_led_every), self.turn_on_led)

    def decrease_brightness(self):
        decrease_brightness(self.strip, self.leds, 0.90)
        self.loop.call_later(ms2s(self.decrease_frequency), self.decrease_brightness)



class PulseCycling:
    def __init__(self, strip, cmap='strandtest_rainbow'):
        self.strip = strip
        self.colors = color_array(cmap, LED_COUNT)
        self.leds = create_rgb_array((LED_COUNT,))
        idx = 0
        while True:
            color = self.colors[idx]
            self.strip.setPixelColor(idx, color24bit(*color))
            self.leds[idx] = color
            strip.show()
            idx = (idx + 1) % LED_COUNT
            sleep_ms(20)
            decrease_brightness(self.strip, self.leds, 0.90)


def create_color_array(length, red_start, red_end, green_start, green_end, blue_start, blue_end):
    #red_start = 100
    #red_end =  255
    #green_start = 0
    #green_end = 255
    #blue_start = 0
    #blue_end = 0
    red = np.linspace(red_start, red_end, length, dtype='int')
    green = np.linspace(green_start, green_end, length, dtype='int')
    blue = np.linspace(blue_start, blue_end, length, dtype='int')
    color_array = create_rgb_array((length,))
    color_array.red = red
    color_array.green = green
    color_array.blue = blue
    return color_array

def plot_color_array(strip):
    colors = create_color_array(LED_COUNT)
    for n in range(LED_COUNT - 1):
        color = color24bit(*colors[n])
        strip.setPixelColor(n, color)
        strip.show()

class Burst:
    def __init__(self, colors):
        self.base_color = colors[0]
        self.peak_color = colors[-1]
        self.colors = colors[1:]
        self.burst_coloring = np.hstack([self.colors, self.colors[-2:0:-1]])
        self.create_fading()

    def create_fading(self):
        fade_steps = 50
        fading_coloring = create_rgb_array((self.burst_coloring.size, fade_steps))
        for n in range(self.burst_coloring.size):
             color_array = create_color_array(
                    fade_steps,
                    red_start=self.burst_coloring[n].red,
                    red_end=self.base_color.red,
                    green_start=self.burst_coloring[n].green,
                    green_end=self.base_color.green,
                    blue_start=self.burst_coloring[n].blue,
                    blue_end=self.base_color.blue
                    ).T
             fading_coloring[n, :] = color_array
        self.fading_coloring = fading_coloring
        self.fade_steps = fade_steps


def plot_burst(strip):
    offset_c = 20
    colors = color_array('strandtest_rainbow', 60)[offset_c: offset_c + 21:4]
    burst = Burst(colors)
    for n in range(LED_COUNT - 1):
        strip.setPixelColor(n, color24bit(*burst.base_color))
        strip.show()
    while True:
        count = 0
        offset = 120#random.randint(burst.burst_coloring.shape[0], LED_COUNT - burst.burst_coloring.shape[0])
        for n in range(offset, offset + burst.burst_coloring.size):
            strip.setPixelColor(n, color24bit(*burst.burst_coloring[count]))
            count += 1
        strip.show()
        sleep_ms(200)

        for k in range(burst.fade_steps):
            count = 0
            for n in range(offset, offset + burst.burst_coloring.size):
                strip.setPixelColor(n, color24bit(*burst.fading_coloring[count, k]))
                count += 1
            strip.show()
            sleep_ms(50)


if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    try:
        loop = asyncio.get_event_loop()
        RandomLightsTurningOnAndFading(loop, strip, cmap='strandtest_rainbow')

        # Blocking call interrupted by loop.stop()
        print('running forever now...')
        loop.run_forever()
        while True:
            print ('Testing....')
            #plot_burst(strip)
            #RandomLightsTurningOnAndFading(strip, cmap='strandtest_rainbow')
            #PulseCycling(strip, cmap='strandtest_rainbow')
            #rainbow(strip, iterations=1)
            #plot_colormap(strip, 'strandtest_rainbow')
            #plot_colormap(strip, 'jet')
            #plot_colormap(strip, 'plasma')
            #plot_colormap(strip, 'prism')
            #plot_colormap(strip, 'summer')
            break
    except KeyboardInterrupt:
        clear(strip)
        loop.close()
