import random
import time
import numpy as np
from matplotlib.pyplot import get_cmap
from rpi_ws281x import Adafruit_NeoPixel


# LED strip configuration:
#LED_COUNT      = 151     # Number of LED pixels.
LED_COUNT      = 60     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10     # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

## NOTE THIS DIFFERS FROM strip/cord LEDs
#            colorWipe(strip, color24bit(255, 0, 0))  # Red wipe (green with cord)
#            colorWipe(strip, color24bit(0, 255, 0))  # Blue wipe
#            colorWipe(strip, color24bit(0, 0, 255))  # Green wipe (red with cord)
CORD_LED = False

def float2int(*args):
    out = list()
    for arg in args:
        out.append(int(round(arg * 255)))
    return tuple(out)


def random_led():
    return random.randint(0, LED_COUNT - 1)


def random_color(colors):
    idx = random.randint(0, colors.shape[0] - 1)
    return colors[idx]


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


def color_array(cmap, length):
    cmap = get_cmap(cmap, length)
    color_array = np.zeros((length, 3), dtype='int')
    for n in range(length):
        r, g, b, _ = cmap(n)
        color_array[n, :] = float2int(r, g, b)
    return color_array

def plot_colormap(strip, cmap):
    print('Plotting colormap: ', cmap)
    if cmap == 'strandtest_rainbow':
        pos = np.linspace(0, 255, LED_COUNT, dtype='int')
        colors = np.zeros((LED_COUNT, 3), dtype='int')
        for idx in range(len(pos)):
            colors[idx, :] = _rainbow(pos[idx])
        #pos = pos.reshape((1, LED_COUNT))
        #colors = np.apply_along_axis(_wheel, 0, pos)
    else:
        colors = color_array(cmap, LED_COUNT)
    print('FARVERNE:', colors)
    for n in range(LED_COUNT - 1):
        color = color24bit(*colors[n,:])
        strip.setPixelColor(n, color)
        strip.show()
    time.sleep(2)


def _rainbow(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)


class RandomLights:
    def __init__(self, strip, cmap='Set1'):
        self.colors = color_array(cmap, 200)
        self.strip = strip
        self.leds = np.zeros((LED_COUNT, 3), dtype='int')
        lights2on = 4
        count = 1
        while True:
            idx = random_led()
            color = random_color(self.colors)
            self.strip.setPixelColor(idx, color24bit(*color))
            self.strip.show()
            self.leds[idx, :] = color
            if count == lights2on:
                self.decrease_brightness()
                count = 1
            else:
                count += 1
            sleep_ms(40)

    def decrease_brightness(self):
        lights_on = np.any(self.leds > 0, axis=1)
        self.leds[lights_on] = self.leds[lights_on] * 0.90
        for n in range(self.leds.shape[0]):
            if lights_on[n]:
                color = color24bit(*self.leds[n,:])
                self.strip.setPixelColor(n, color)
        strip.show()


if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    try:
        while True:
            print ('Testing....')
            #RandomLights(strip)
            #rainbow(strip, iterations=1)
            plot_colormap(strip, 'strandtest_rainbow')
            #plot_colormap(strip, 'jet')
            #plot_colormap(strip, 'plasma')
            #plot_colormap(strip, 'rainbow')
            #plot_colormap(strip, 'prism')
            #plot_colormap(strip, 'terrain')
            #plot_colormap(strip, 'Set1')
            #plot_colormap(strip, 'summer')
            break
    except KeyboardInterrupt:
        clear(strip)
