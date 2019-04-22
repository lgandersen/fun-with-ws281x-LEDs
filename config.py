# LED strip configuration:
LED_COUNT = 500     # Number of LED pixels.
#LED_COUNT = 330     # Number of LED pixels.
#LED_COUNT = 60     # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN = 21     # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

## NOTE Different color encoding with strip/cord LEDs
# (255, 0, 0) Red wipe (green with cord)
# (0, 255, 0) Blue wipe
# (0, 0, 255) Green wipe (red with cord)
# Use setting below to denote which type of LED-device is being used.

WS2811 = True # If false it is assumed to be WS2812 (strip)
