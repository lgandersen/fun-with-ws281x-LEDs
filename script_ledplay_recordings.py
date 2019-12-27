import pandas as pd

from player import LEDPlayer
from config import RECORDING_FILE

if __name__ == '__main__':
    df = pd.read_pickle(RECORDING_FILE)
    df.sort_values(['itensity', 'roc'], inplace=True)
    df.head()
    #df = df[df['itensity'] > df.describe()['itensity']['75%']]
    print(df.head())
    streams = list(df['stream'])
    streams.reverse()
    print('Press Ctrl-C to quit.')
    #player = Player(turn_off)
    player = LEDPlayer(streams)
    player.start()
