import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# print(os.listdir('/Users/Ashley/Desktop/'))
file_name = '/Users/Ashley/Desktop/decimated.csv'
df = pd.read_csv(file_name)
tracks = df['TRACK_ID']
tracks = tracks.str.replace('None', '0', case=False)
tracks = np.int16(tracks)
print(np.max(tracks))

hold_traces = []
for I in range(np.max(tracks)):
    out = (df.loc[df['TRACK_ID'] == str(I)])
    df1 = out.iloc[:, 4:6]
    hold_traces.append(np.asarray(df1))

plt.plot(hold_traces[4][:, 0], hold_traces[4][:, 1])
plt.show()
