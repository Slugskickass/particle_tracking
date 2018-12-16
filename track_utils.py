import pandas as pd
import numpy as np



def get_track(file_name, track_number):
    df = pd.read_csv(file_name)
    out = (df.loc[df['TRACK_ID'] == str(track_number)])
    df1 = out.iloc[:, 4:6]
    coordinates = np.asarray(df1)
    return coordinates

def get_number_tracks(file_name):
    df = pd.read_csv(file_name)
    tracks = df['TRACK_ID']
    tracks = tracks.str.replace('None', '0', case=False)
    return np.max(tracks)

def get_longest_track(file_name):
    df = pd.read_csv(file_name)
    tracks = df['TRACK_ID']
    tracks = tracks.str.replace('None', '0', case=False)
    out = 0
    position = 0
    for track_number in tracks:
        data = (df.loc[df['TRACK_ID'] == str(track_number)])
        if data.shape[0] > out:
            position = track_number
            out = data.size
    return position, out
