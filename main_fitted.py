import Stack as Stack
import NDR_Tracking as ndrt
import numpy as np
import imageio
import os
import time
from multiprocessing import Pool

if __name__ == '__main__':
    ####
    # The settings for the code
    # For sliding set cut_offset = 1
    ####
    # For decimated set cut_offset = 10

    slice_size = 10                     # This is the number of frames to fit
    start_block = 0                     # This is the block to start at
    cut_offset = 10                     # This is the offset between the last cut and this one
    file_name = './Untitled013.tsm'     # This is the frame to load

    #####



    Image_stack = Stack.Stack(file_name)                 # This defines the data as a class which provides some advantages

    print('The Image is ' + str(Image_stack.height) + ' by ' + str(Image_stack.width) + ' Pixels')
    print('With ' + str(np.uint16(Image_stack.nframes)) + ' Frames')
    print('The first block starts at the ' + str(Image_stack.starting_value) + ' frame')
    print('The length of a stack is ' + str(Image_stack.difference))
    print('There are ' + str(Image_stack.number_of_stacks) + ' Blocks in the file')


    if cut_offset == 10:
        file_name_save = 'Decimated'
    else:
        file_name_save = 'Sliding'

    pool = Pool(processes=10)
    for block_number in range(start_block, Image_stack.number_of_stacks, 1):
        hold = []
        data_main = Image_stack.load_block(block_number)
        start_time = time.clock()
        for I in range(slice_size, Image_stack.difference, cut_offset):
            data = data_main[I - slice_size:I, :, :]
            data_out = ndrt.fitted_decimate_single_black(data, pool)
            hold.append(data_out)
        print(block_number)
        filename = file_name_save + format(block_number, "05d")
        hold = np.asarray(hold)
        end_time = time.clock()
        print(end_time - start_time)
        np.save(filename, hold)
        del hold
        del data
        del data_out
        del data_main
