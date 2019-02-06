import Stack as Stack
import NDR_Tracking as ndrt
import numpy as np
import imageio
import os
import time
from multiprocessing import Pool
from multiprocessing import get_context

if __name__ == '__main__':
    print(os.listdir('./'))
    #  file_name = '/Users/Ashley/Desktop/25percbeads100RDIVIDE2.tsm'
    file_name = '/Users/Ashley/Desktop/Untitled014.tsm'

    Image_stack=Stack.Stack(file_name)                 # This defines the data as a class which provides some advantages

    print('The Image is ' + str(Image_stack.height) + ' by ' + str(Image_stack.width) + ' Pixels')
    print('With ' + str(np.uint16(Image_stack.nframes)) + ' Frames')
    print('The first block starts at the ' + str(Image_stack.starting_value) + ' frame')
    print('The length of a stack is ' + str(Image_stack.difference))
    print('There are ' + str(Image_stack.number_of_stacks) + ' Blocks in the file')

    slice_size = 10
    start_block = 0
    end_block = 10 # 99

    # decimated data
    #final_data_dec = ndrt. decimate_data(Image_stack, slice_size, start_block, end_block)
    #imageio.mimwrite('decimated.tiff', final_data_dec)
    #del final_data_dec

    # sliding data
    #final_data_slide = ndrt.slidding_data(Image_stack, slice_size, start_block, end_block)
    #imageio.mimwrite('sliding.tiff', final_data_slide, bigtiff=True)
    #del final_data_slide

    # fitted decimated data
    start_time = time.clock()
    pool = Pool(processes=10)
    hold = []
    for block_number in range(start_block, end_block, 1):
        data_main = Image_stack.load_block(block_number)
        end_time = time.clock()
        print(end_time - start_time)
        start_time = time.clock()
        for I in range(10, 100, 1):
            data_out = ndrt.fitted_decimate_single_black(data_main[I-10:I, :, :], pool)
            hold.append(data_out)
            print(I)
    hold = np.asarray(hold)
    np.save('slidingcv  ', hold)
    # a = np.float32(outer)
    # imageio.mimwrite('testb.tiff', a, bigtiff=True)

    #final_data_fitted_dec = ndrt.fitted_decimate_data(Image_stack, slice_size, start_block, end_block)
    #imageio.mimwrite('decimated_fitted.tiff', hold, bigtiff=True)

    # fitted sliding_data
    # final_data_fitted_dec = ndrt.fitted_decimate_data(Image_stack, slice_size, start_block, end_block)

    # imageio.mimwrite('sliding.tiff', final_data_fitted_sliding
