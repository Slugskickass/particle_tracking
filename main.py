import Stack as Stack
import NDR_Tracking as ndrt
import numpy as np
import imageio
import os

print(os.listdir('./'))
#  file_name = '/Users/Ashley/Desktop/25percbeads100RDIVIDE2.tsm'
file_name = './25percbeads100RDIVIDE2.tsm'

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
final_data_dec = ndrt. decimate_data(Image_stack, slice_size, start_block, end_block)
imageio.mimwrite('decimated.tiff', final_data_dec)
del final_data_dec

# sliding data
final_data_slide = ndrt.slidding_data(Image_stack, slice_size, start_block, end_block)
imageio.mimwrite('sliding.tiff', final_data_slide, bigtiff=True)
del final_data_slide

# fitted decimated data
#final_data_fitted_dec = ndrt.fitted_decimate_data(Image_stack, slice_size, start_block, end_block)
#imageio.mimwrite('decimated_fitted.tiff', final_data_fitted_dec, bigtiff=True)

# fitted sliding_data
# final_data_fitted_dec = ndrt.fitted_decimate_data(Image_stack, slice_size, start_block, end_block)

# imageio.mimwrite('sliding.tiff', final_data_fitted_sliding
