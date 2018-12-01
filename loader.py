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

a = list_files(directory, 'npy')

data =[]
for file_name in a:
    data.extend(np.load(file_name))
print(np.shape(data))
print(type(data))
data = np.asarray(data)
print(type(data))
data = np.float32(data)
#imageio.mimwrite('decimated_fitted.tiff', data)
