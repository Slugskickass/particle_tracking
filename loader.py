import os
import numpy as np
import imageio
directory = './'


def list_files(directory, ending):
    files = os.listdir(directory)
    list = []
    for file in files:
        if file.endswith(ending):
            list.append(file)
    return list


a = list_files(directory, '.npy')
a.sort()
data = []
for file_name in a:
    print(file_name)
    temp = np.load(file_name)
    temp = np.float32(temp)
    data.extend(temp)
imageio.mimwrite('sliding_fitted.tiff', data, bigtiff=True)
