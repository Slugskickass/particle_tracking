import Stack as Stack
import NDR_Tracking as ndrt
import numpy as np
import imageio
import os
import time

print(os.listdir('./'))
#  file_name = '/Users/Ashley/Desktop/25percbeads100RDIVIDE2.tsm'
file_name = './25percbeads100RDIVIDE2.tsm'

Image_stack = Stack.Stack(file_name)                 # This defines the data as a class which provides some advantages

print('The Image is ' + str(Image_stack.height) + ' by ' + str(Image_stack.width) + ' Pixels')
print('With ' + str(np.uint16(Image_stack.nframes)) + ' Frames')
print('The first block starts at the ' + str(Image_stack.starting_value) + ' frame')
print('The length of a stack is ' + str(Image_stack.difference))
print('There are ' + str(Image_stack.number_of_stacks) + ' Blocks in the file')

hold = []
final_hold = []
start_time = time.clock()
for J in range(10):
    data_main = Image_stack.load_block(J)
    for I in range(10, 100, 10):
        data = data_main[I-10:I, :, :]
        data_out = ndrt.fitted_decimate_single_black(data)
        hold.append(data_out)
    print(J)
    final_hold.append(hold)
print(time.clock()-start_time)
print(np.shape(final_hold))
final_hold = np.float32(np.asarray(final_hold))
imageio.mimwrite('decimated_fitted.tiff', final_hold, bigtiff=True)
