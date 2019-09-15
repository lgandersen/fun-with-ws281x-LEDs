from time import sleep, time as tick

from config import FPS, SWITCH_RATE

from strip import set_colors_all


class _Delay:
    """ Adjusts the delay that is used to sleep between each frame
        to keep the FPS fixed independently of the number of LED's attached. """
    def __init__(self):
        self._delay = 0
        self.expect_frame_creation_time = 1 / FPS # What is the time it should take to create a frame to keep at FPS frames/sec
        self.t_start = tick()

    def __call__(self):
        return self._delay

    def update(self):
        t_end = tick()
        fps = 1 / (t_end - self.t_start)
        frame_creation_time = 1/fps
        remaining_time = max(0, (self.expect_frame_creation_time - frame_creation_time)) # If slower theres is nothing to do! :(
        # We add only half so we approach to true value instead of giving exact estimate (increases stability):
        self._delay += remaining_time / 2
        self.t_start = tick()


class Player:
    def __init__(self, streams):
        self.streams = streams
        self.fps_counter = 0
        self.stream_idx = 0

    def start(self):
        delay = _Delay()
        self.next_stream()

        while True:
            offset = 1
            for n, frame in enumerate(self.stream, offset):
                self.fps_counter += 1
                set_colors_all(frame)
                sleep(delay())
                delay.update()

                if n % (SWITCH_RATE * FPS) == 0:
                    break

                if n % (2 * FPS) == 0:
                    self.calc_fps()


            self.next_stream()
            offset = n + 1

    def next_stream(self):
        print('Changing to stream ', self.stream_idx, self.streams[self.stream_idx])
        self.stream = self.streams[self.stream_idx]
        self.stream_idx = (self.stream_idx + 1) % len(self.streams)

    def calc_fps(self):
        print('Playing with {:.2f} fps per second'.format(self.fps_counter / 2))
        self.fps_counter = 0
