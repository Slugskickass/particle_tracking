import Stack as Stack
import NDR_Tracking as ndrt
import numpy as np
import imageio
import os
import time
from multiprocessing import Pool

if __name__ == '__main__':
    ####
    # For sliding set cut_offset = 1
    ####
    # For decimated set cut_offset = 10
    print(os.listdir('./'))
    #  file_name = '/Users/Ashley/Desktop/25percbeads100RDIVIDE2.tsm'
    file_name = '/Users/Ashley/Desktop/Untitled014.tsm'

    Image_stack = Stack.Stack(file_name)                 # This defines the data as a class which provides some advantages

    print('The Image is ' + str(Image_stack.height) + ' by ' + str(Image_stack.width) + ' Pixels')
    print('With ' + str(np.uint16(Image_stack.nframes)) + ' Frames')
    print('The first block starts at the ' + str(Image_stack.starting_value) + ' frame')
    print('The length of a stack is ' + str(Image_stack.difference))
    print('There are ' + str(Image_stack.number_of_stacks) + ' Blocks in the file')

    slice_size = 10
    start_block = 0
    end_block = 10 # 99


    cut_offset = 10
    if cut_offset == 10:
        file_name_save = 'Decimated'
    else:
        file_name_save = 'Sliding'

    pool = Pool(processes=10)
    for block_number in range(start_block, end_block, 1):
        hold = []
        data_main = Image_stack.load_block(block_number)
        start_time = time.clock()
        for I in range(10, 100, cut_offset):
            data = data_main[I - 10:I, :, :]
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
