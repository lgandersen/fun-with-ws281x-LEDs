import asyncio
from random import randint

import numpy as np

from config import LED_COUNT
from utils import create_color_array, RGB
from strip import set_colors_all

def iter_pulse_cycling_configs(limit=999999):
    frames_cmap = [
            create_color_array('strandtest_rainbow', LED_COUNT),
            create_color_array('prism', LED_COUNT),
            create_color_array('jet', LED_COUNT),
            ]
    frames_constant = [
            create_color_array(tuple(color), LED_COUNT)
            for color in create_color_array('strandtest_rainbow', 10)
            ]

    cfg_tmplate = {
            'base_frame':create_color_array('strandtest_rainbow', LED_COUNT),
            'offsets':np.arange(0, LED_COUNT, 25), # offsets (and number) of pulses
            'fading_frame':create_color_array(RGB(r=0, g=0, b=0), LED_COUNT),
            'fade_rate':0.50,
            'fade_freq':10, # [ms]
            'turn_on_freq':0, #[ms]
            }

    count = 0
    while count < limit:
        cfg = dict(cfg_tmplate)

        if randint(0, 1) == 1:
            cfg['fading_frame'] = frames_constant[randint(0, 9)]
        else:
            cfg['fading_frame'] = create_color_array(RGB(r=0, g=0, b=0), LED_COUNT)


        cfg['base_frame'] = frames_cmap[randint(0, 2)]

        offset_step = randint(20, 100)
        cfg['offsets'] = np.arange(0, LED_COUNT, offset_step)

        fade_rate = randint(1, 5)/10
        cfg['fade_rate'] = fade_rate

        cfg['turn_on_freq'] = randint(0, 500) * fade_rate


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
        #self.play_frames_from_queue()
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
