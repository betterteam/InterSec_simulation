import math
from numpy import *

def new_rec(x, y, r):
    a = mat([[math.cos(math.radians(r)), -math.sin(math.radians(r))],
               [math.sin(math.radians(r)), math.cos(math.radians(r))]])

    b = mat([[x],
             [y]])

    c = mat([[5],
             [2.5]])

    res = a * (b - c) + c

    return float(res[0][0]), float(res[1][0])


a = new_rec(10, 0, 0)
print(a)