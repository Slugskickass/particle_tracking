import numpy as np
import sys
import os


class Stack(object):
    """
    Image stack object for holding and collating an NDR dataset
    Stack class is called with the filename as the constructor,
    the class automatically will run through the data obtaining
    the width, height, number of frames, location of the first reset,
    and the difference between resets.

    Useful functions:
    get_frame(frame_number) - returns the image data from a particular frame
    get_pixel_trace(start_frame_number, end_frame_number, x_pixel, y_pixel) - returns the time trace for a particular
        pixel between start and end

    """
# this changed for number of frames
    def __init__(self, filename):
        self.filename = filename
        self.width, self.height, self.nframes = self.getfiledata()
        if self.nframes > 1000:
            number_of_frames = 300
        else:
            number_of_frames = self.nframes
        self.starting_value, self.difference = self.find_resets(0, number_of_frames, 1)
        self.number_of_stacks = np.uint16(np.floor(np.float((self.nframes - self.starting_value) / self.difference)))

    def getfiledata(self):
        with open(self.filename, 'rb') as f:
            f.seek(266)
            data = f.read(16)
            width_im = int(data.decode('utf-8'))
            f.seek(347)
            data = f.read(16)
            height_im = int(data.decode('utf-8'))
            f.seek(425)
            data = f.read(16)
            number_frames = int(data.decode('utf-8'))
        f.close()
        return width_im, height_im, number_frames

    def get_frame(self, frame_number):
        with open(self.filename, 'rb') as f:
            f.seek(frame_number * (self.width * self.height * 2) + 2880)
            data = f.read(self.width * self.height * 2)
        f.close()
        frame = np.fromstring(data, dtype=np.uint16).reshape(self.height, self.width)
        return frame

    def find_resets_old(self, number_frames):
        holdall = []
        self.printProgress(0, int(number_frames), prefix='Progress:', suffix='Complete', barLength=50)
        for i in range(0, int(number_frames)):
            image = self.get_frame(i)
            self.printProgress(i, number_frames, prefix='Progress:', suffix='Complete', barLength=50)
            holdall.append(np.sum(np.sum(image, axis=1), axis=0))
        temper = np.absolute(np.diff(holdall))
        maxi_value = 0.5 * np.max(temper)
        selected_points = np.where(temper > maxi_value)
        selected_points = np.array(selected_points)
        starting_value = selected_points[0][0]
        differences = np.diff(selected_points)
        points = np.where(differences > 10)
        difference = 0
        if np.mean(differences[points]) > 498 and np.mean(differences[points]) < 502:
            difference = 500
        if np.mean(differences[points]) > 98 and np.mean(differences[points]) < 102:
            difference = 100
        return starting_value, difference

    def printProgress(self, iteration, total, prefix='', suffix='', decimals=1, barLength=100, fill='0'):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            barLength   - Optional  : character length of bar (Int)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(int(barLength) * int(iteration) // int(total))
        bar = fill * filledLength + '-' * (barLength - filledLength)
        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
        if iteration == total:
            sys.stdout.write('\n')
        sys.stdout.flush()

    # This block loader does not work.
    def load_block(self, blocknum):
        with open(self.filename, 'rb') as f:
            #f.seek((blocknum * self.difference + self.starting_value) * (self.width * self.height * 2) + 2880)
            f.seek(2880 + (self.starting_value * self.width * self.height * 2) + (
                blocknum * self.difference * self.width * self.height * 2))
            data = f.read(self.width * self.height * 2 * self.difference)
        f.close()
        block = np.fromstring(data, dtype=np.uint16).reshape(self.difference, self.height, self.width)
        return block

    def get_pixel_trace(self, start_frame_number, end_frame_number, x_pixel, y_pixel):
        trace = []
        with open(self.filename, 'rb') as f:
            for frame_number in range(start_frame_number, end_frame_number):
                f.seek(2880 + 2 * ((frame_number * self.width * self.height) + (y_pixel * self.width) + x_pixel))
                data = f.read(2)
                trace.append(np.fromstring(data, dtype=np.uint16))
        f.close()
        return trace

    def get_line_trace(self, start_frame_number, end_frame_number, line_number):
        trace = []
        with open(self.filename, 'rb') as f:
            for frame_number in range(start_frame_number, end_frame_number):
                f.seek(2880 + 2 * ((frame_number * self.width * self.height) + (line_number * self.height)))
                data = f.read(self.width * 2)
                trace.append(np.fromstring(data, dtype=np.uint16))
        f.close()
        return trace

    def find_resets(self, start_frame_number, end_frame_number, line_number):
        line_data = self.get_line_trace(start_frame_number, end_frame_number, line_number)
        mean_line_data = np.absolute(np.diff(np.mean(line_data, axis=1)))
        mean_value = np.mean(mean_line_data)
        selected_points = np.array(np.where(mean_line_data > 10 * mean_value))
        diff_points = np.diff(selected_points[0])
        selected_points = 1 + selected_points[0][0]
        diff_points = np.int16(np.mean(diff_points))
        return selected_points, diff_points



if __name__ == "__main__":
    path = "Untitled021.tsm"
    imstack = Stack(path)
    print("Height: " + str(imstack.height))
    print("Width: " + str(imstack.width))
    print("Number of Frames: " + str(imstack.nframes))
    print(imstack.difference)
    frame = imstack.load_block(5)
    print(frame.shape)
