import Stack as Stack
import numpy as np
from scipy import stats
import time
from multiprocessing import Pool
from multiprocessing import get_context

def fit_line(line_data):
    cut_section_length = 10
    line_length = np.size(line_data, axis=1)
    hold_all = np.zeros(line_length)
    x = np.linspace(0, cut_section_length, cut_section_length)
    for I in range(line_length):
        y = line_data[:, I]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        hold_all[I] = slope
    return hold_all


def decimate_data(Image_stack, slice_size, start_block, end_block):
    print('decimate')
    final_data = []
    for block_of_interest in range(start_block, end_block, 1):
        data = Image_stack.load_block(block_of_interest)
        for I in range(slice_size, Image_stack.difference, slice_size):
            final_data.append(np.float32(np.float32(data[I, :, :]) - np.float32(data[I-slice_size, :, :])))
    final_data = np.asarray(final_data)
    return final_data


def slidding_data(Image_stack, slice_size, start_block, end_block):
    print('sliding')
    final_data = []
    for block_of_interest in range(start_block, end_block, 1):
        data = Image_stack.load_block(block_of_interest)
        for I in range(slice_size, Image_stack.difference, 1):
            final_data.append(np.float32(np.float32(data[I, :, :]) - np.float32(data[I-slice_size, :, :])))
    final_data = np.asarray(final_data)
    return final_data

def fitted_decimate_data(Image_stack, slice_size, start_block, end_block):
    print('fitted')
    final_data = []
    #x_line = np.linspace(0, slice_size, slice_size)
    for block_of_interest in range(start_block, end_block, 1):
        print(block_of_interest)
        data = Image_stack.load_block(block_of_interest)
        for I in range(slice_size, Image_stack.difference, slice_size):
#            linear_hold = np.zeros([Image_stack.height, Image_stack.width])
#            temp_data = (np.float32(data[I-slice_size:I, :, :]))
#            start_time = time.time()
            result = []
#            start_time = time.clock()
            for X in range(Image_stack.height):
                result.append(data[0:10, X, :])
                # slope, intercept, r_value, p_value, std_err = stats.linregress(x_line, temp_data[:, X, Y])
            pool = Pool(processes=10)
            final_hold_a = pool.map(fit_line, result)
#            print(time.clock() - start_time)
            #if (np.ndim(final_hold_a)) == 2:
            #    final_hold_a = np.expand_dims(final_hold_a, axis=2)
            #final_data = np.append(final_data, final_hold_a, axis=2)
        final_data.append(final_hold_a)
        print(np.shape(final_data))

    # change list to array
    final_data = np.float32(np.asarray(final_data))
    return final_data


def fitted_decimate_single_black(data, pool):
    with get_context("spawn").Pool() as pool:
        result = []
        for X in range(456): # change this to the data height
            result.append(data[0:10, X, :])
    #    pool = Pool(processes=10)
        final_data = pool.map(fit_line, result)
    return final_data


def fitted_sliding_single_black(data, pool):
    result = []
    for X in range(456): # change this to the data height
        result.append(data[0:10, X, :])
#    pool = Pool(processes=10)
    final_data = pool.map(fit_line, result)
    return final_data

# def fitted_slidding_data(Image_stack, slice_size, start_block, end_block):
#     final_data = []
#     for block_of_interest in range(start_block, end_block, 1):
#         data = Image_stack.load_block(block_of_interest)
#         for I in range(slice_size, Image_stack.difference, slice_size):
#             result = []
#             start_time = time.clock()
#             for X in range(Image_stack.height):
#                 result.append(data[0:10, X, :])
#             pool = Pool(processes=10)
#             final_hold_a = pool.map(fit_line, result)
#             print(np.shape(final_hold_a))
#         final_data.append(linear_hold)
#         print(time.clock() - start_time)
#     return


