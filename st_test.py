import numpy as np
import numba
import time
import Stack as Stack
from scipy import stats

@numba.njit
def cov(x, y):
    return (x*y).mean() - (x.mean() * y.mean())


@numba.njit
def binregress(x, y):
    """
    Calculate a regression line, based on scipy

    """
    xmean = np.mean(x)
    ymean = np.mean(y)

    # average sum of squares
    ssxm, ssxym = cov(x, x), cov(x, y)
    r_num = ssxym
    slope = r_num / ssxm
    intercept = ymean - slope*xmean
    return slope, intercept


file_name = '25percbeads100RDIVIDE2.tsm'
Image_stack = Stack.Stack(file_name)
data_main = Image_stack.load_block(1)
x = np.linspace(0,10,10)
y = data_main[0:10, 10, 10]
slope = 0
intercept = 0

one = time.clock()
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
two = time.clock()
print(two - one)

three = time.clock()
slope, intercept = binregress(x, y)
four = time.clock()
print(four - three)
print((four - three)/(two - one))