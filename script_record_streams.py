import numpy as np
import pandas as pd

from player import record_stream
from stream_generators import all_streams
from config import RECORDING_FILE

def calc_intensity(recording):
    return sum([recording.red.mean(), recording.green.mean(), recording.blue.mean()])

def calc_rate_of_change(recording):
    rate_of_change = lambda x: np.abs(np.diff(x, axis=0)).mean()
    change = sum([
        rate_of_change(recording.red),
        rate_of_change(recording.green),
        rate_of_change(recording.blue),
        ])
    return change

stats = []

def iter_recordings(n, stream):
    recording = record_stream(stream, nframes=3600)
    intensity = calc_intensity(recording)
    rate_of_change = calc_rate_of_change(recording)
    print('{} Intensity, rate of change: {:.2f}, {:.2f}'.format(n, intensity, rate_of_change))
    return (stream, intensity, rate_of_change)

if __name__ == '__main__':
    from joblib import Parallel, delayed
    streams = [stream for stream in all_streams(10000)]
    recordings = Parallel(n_jobs=2)(delayed(iter_recordings)(n, stream) for n, stream in enumerate(streams))
    df = pd.DataFrame(recordings, columns = ['stream', 'itensity', 'roc'])
    df.to_pickle(RECORDING_FILE)

