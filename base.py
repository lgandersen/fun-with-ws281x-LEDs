import asyncio

from strip import clear_all, set_colors_all
from utils import create_color_array, RGB
from config import LED_COUNT


def morph_frame(base_frame, frame2morph, fade_rate):
    red, green, blue = base_frame.red, base_frame.green, base_frame.blue

    frame2morph.red = frame2morph.red + (red - frame2morph.red) * fade_rate
    frame2morph.green = frame2morph.green + (green - frame2morph.green) * fade_rate
    frame2morph.blue = frame2morph.blue + (blue - frame2morph.blue) * fade_rate
    return frame2morph

class LEDConfigurationBase:
    frame = create_color_array(RGB(r=0, g=0, b=0), LED_COUNT)

    def __init__(self, **kwargs):
        self.queue = kwargs['queue']
        for parameter in self.parameters:
            try:
                setattr(self, parameter, kwargs[parameter])
            except:
                raise Exception("Parameter '{}' was not provided.".format(parameter))

        self._loop = asyncio.get_event_loop()
        self._stop = False
        self.create_task(self.submit_frame)

    def stop(self):
        self._stop = True

    def call_later(self, delay_ms, callback, *args):
        if self._stop:
            return
        self._loop.call_later(delay_ms / 1000, callback, *args) # convert to second

    def create_task(self, coroutine):
        if self._stop:
            return
        self._loop.create_task(coroutine())

    async def sleep(self, ms):
        await asyncio.sleep(ms / 1000)

    def draw_frame(self):
        set_colors_all(self.frame)

    async def submit_frame(self):
        await self.queue.put(self.frame)
        self.create_task(self.submit_frame)

    def __del__(self):
        clear_all()
        print("I'm fading, Dave.")
