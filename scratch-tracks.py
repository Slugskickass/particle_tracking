import track_utils as tu
import numpy as np
import matplotlib.pyplot as plt

file_name ='/Users/Ashley/Desktop/NDR_tracker/Decimated.csv'
tracks_dec = tu.get_track(file_name, 1)

file_name ='/Users/Ashley/Desktop/NDR_tracker/Decimated_fitted.csv'
tracks_dec_fit = tu.get_track(file_name, 6)

print(np.shape(tracks_dec))
print(np.shape(tracks_dec_fit))

#plt.plot(tracks_dec[:, 0], tracks_dec[:, 1])
#plt.plot(tracks_dec_fit[:, 0], tracks_dec_fit[:, 1])
#plt.show()