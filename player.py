import asyncio
from random import randint

import numpy as np
from numpy.random import choice as choose

from config import LED_COUNT
from utils import RGB
from strip import set_colors_all
from colormap import create_colormap, create_colormap_slice


def _choose_cmap_frame(frames_cmap):
    return frames_cmap[choose(len(frames_cmap))]


def _no_lights_or_random_cmap(frames_cmap, likelihood=2):
    if randint(0, likelihood) == 0:
        cmap = create_colormap(RGB(r=0, g=0, b=0), LED_COUNT)
    else:
        cmap = frames_cmap[choose(len(frames_cmap))]
    return cmap


def iter_random_lights_turning_on_configs(limit=99999):
    frames_cmap = [
        create_colormap('strandtest_rainbow', LED_COUNT),
        create_colormap('prism', LED_COUNT),
        create_colormap('jet', LED_COUNT),
    ]
    random_widths = [
        (2, 2),
        (1, 5),
        (5, 10),
        (5, 25)
        ]
    count = 0
    while count < limit:
        cfg = {
            'shuffle':choose([True, False]),
            'palettes':_choose_cmap_frame(frames_cmap),
            'random_width':random_widths[choose(len(random_widths))],# Tuple (start, end) of random sampled widths (start == end implies fixed width)
            'fading_frame':create_colormap(RGB(r=0, g=0, b=0), LED_COUNT),
            'fade_rate':choose([0, 0.005, 0.01, 0.10]),
            'turn_on_freq':choose([0, 0, 50, 100]),
            }
        yield cfg
        count += 1


def iter_pulse_cycling_configs(limit=999999):
    frames_cmap = [
        create_colormap('strandtest_rainbow', LED_COUNT),
        create_colormap('prism', LED_COUNT),
        create_colormap('jet', LED_COUNT),
        ] + [
        create_colormap(tuple(color), LED_COUNT)
        for n, color in enumerate(create_colormap('strandtest_rainbow', 20))
        if n % 2 == 0
        ]
    count = 0
    while count < limit:
        cfg = {
            'fading_frame':_no_lights_or_random_cmap(frames_cmap),
            'base_frame':frames_cmap[choose(len(frames_cmap))],
            'offsets':np.arange(0, LED_COUNT, choose([25, 40, 75, 100])),
            'fade_rate':choose([0.05, 0.01, 0.05, 0.10, 0.20]),
            'turn_on_freq':choose([0, 0, 50, 100]),
            'turn_on_at_once':choose([1, 1, 2, 4, 6]),
            }
        yield cfg
        count += 1


class Player:
    def __init__(self, workbooks):
        self.switch_rate = 10
        self.fps_counter = 0
        self.workbooks = workbooks

        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue(maxsize=100)

        workbook, cfg = self.workbooks[0]
        self.present_workbook = workbook(queue=self.queue, **cfg)
        self.workbook_idx = 1 % len(self.workbooks)

    def start(self):
        self.change_workbook()
        self.loop.create_task(self.play_frames_from_queue())
        self.loop.call_later(2, self.calc_fps) # convert to second
        self.loop.run_forever()

    async def play_frames_from_queue(self):
        while True:
            #t1 = time.time()
            frame = await self.queue.get()
            #print('Frame fetched in {:.3f} seconds.'.format(time.time() - t1))
            #t2 = time.time()
            set_colors_all(frame)
            #print('Frame drawed in {:.3f} seconds.'.format(time.time() - t2))
            self.fps_counter += 1

    def change_workbook(self):
        self.present_workbook.stop()
        last_frame = self.present_workbook.frame

        print('Changing to workbook ', self.workbook_idx, self.workbooks[self.workbook_idx][0])
        workbook, cfg = self.workbooks[self.workbook_idx]
        self.present_workbook = workbook(queue=self.queue, **cfg)
        if last_frame is not None:
            self.present_workbook.frame = last_frame
        self.workbook_idx = (self.workbook_idx + 1) % len(self.workbooks)
        self.loop.call_later(self.switch_rate, self.change_workbook)

    def calc_fps(self):
        print('Playing with {:.2f} fps per second'.format(self.fps_counter / 2))
        self.fps_counter = 0
        self.loop.call_later(2, self.calc_fps) # convert to second
