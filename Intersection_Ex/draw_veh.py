# coding:utf-8
# Functions that could be used to calculate the big rectangle
# Used From IM_2_2; veh_2_2

from numpy import *

# Calculate rectangle's new position by using Center Point
def new_rec(c_x, c_y, x, y, r):
    a = mat([[math.cos(math.radians(r)), -math.sin(math.radians(r))],
               [math.sin(math.radians(r)), math.cos(math.radians(r))]])

    b = mat([[x],
             [y]])

    c = mat([[c_x],
             [c_y]])

    res = a * (b - c) + c

    return float(res[0][0]), float(res[1][0])


# begin as a vertical rectangle
# center_x position, center_y position and rotation angle
def new_v_rec(qp, c_x, c_y, r):
    up_left = (c_x - 5 / 2, c_y - 10 / 2)
    up_right = (c_x + 5 / 2, c_y - 10 / 2)
    down_left = (c_x - 5 / 2, c_y + 10 / 2)
    down_right = (c_x + 5 / 2, c_y + 10 / 2)

    new_up_left = new_rec(c_x, c_y, up_left[0], up_left[1], r)
    new_up_right = new_rec(c_x, c_y, up_right[0], up_right[1], r)
    new_down_left = new_rec(c_x, c_y, down_left[0], down_left[1], r)
    new_down_right = new_rec(c_x, c_y, down_right[0], down_right[1], r)

    qp.drawLine(new_up_left[0], new_up_left[1], new_up_right[0], new_up_right[1])
    qp.drawLine(new_up_left[0], new_up_left[1], new_down_left[0], new_down_left[1])
    qp.drawLine(new_up_right[0], new_up_right[1], new_down_right[0], new_down_right[1])
    qp.drawLine(new_down_left[0], new_down_left[1], new_down_right[0], new_down_right[1])
    # return new_up_left, new_up_right, new_down_left, new_down_right


# begin as a tropical rectangle
# center_x position, center_y position and rotation angle
def new_t_rec(qp, c_x, c_y, r):
    up_left = (c_x - 10 / 2, c_y - 5 / 2)
    up_right = (c_x + 10 / 2, c_y - 5 / 2)
    down_left = (c_x - 10 / 2, c_y + 5 / 2)
    down_right = (c_x + 10 / 2, c_y + 5 / 2)

    new_up_left = new_rec(c_x, c_y, up_left[0], up_left[1], r)
    new_up_right = new_rec(c_x, c_y, up_right[0], up_right[1], r)
    new_down_left = new_rec(c_x, c_y, down_left[0], down_left[1], r)
    new_down_right = new_rec(c_x, c_y, down_right[0], down_right[1], r)

    qp.drawLine(new_up_left[0], new_up_left[1], new_up_right[0], new_up_right[1])
    qp.drawLine(new_up_left[0], new_up_left[1], new_down_left[0], new_down_left[1])
    qp.drawLine(new_up_right[0], new_up_right[1], new_down_right[0], new_down_right[1])
    qp.drawLine(new_down_left[0], new_down_left[1], new_down_right[0], new_down_right[1])
    # return new_up_left, new_up_right, new_down_left, new_down_right



















































# Turning from West to South
def W2S_up_left_x(po_x, r):
    return po_x - 5 * math.sin(math.radians(r))


def W2S_up_left_y(po_y):
    return po_y


def W2S_up_right_x(po_x, r):
    return po_x + 10 * math.cos(math.radians(r))


def W2S_up_right_y(po_y):
    return po_y


def W2S_down_left_x(po_x, r):
    return po_x - 5 * math.sin(math.radians(r))


def W2S_down_left_y(po_y, r):
    return po_y + 5 * math.cos(math.radians(r)) + 10 * math.sin(math.radians(r))


def W2S_down_right_x(po_x, r):
    return po_x + 10 * math.cos(math.radians(r))


def W2S_down_right_y(po_y, r):
    return po_y + 10 * math.sin(math.radians(r)) + 5 * math.cos(math.radians(r))

# Turning from South to West
def S2W_up_left_x(po_x):
    return po_x


def S2W_up_left_y(po_y, r):
    return po_y - 5 * math.sin(math.radians(r))


def S2W_up_right_x(po_x, r):
    return po_x + 10 * math.sin(math.radians(r)) + 5 * math.cos(math.radians(r))


def S2W_up_right_y(po_y, r):
    return po_y - 5 * math.sin(math.radians(r))


def S2W_down_left_x(po_x):
    return po_x


def S2W_down_left_y(po_y, r):
    return po_y + 10 * math.cos(math.radians(r))


def S2W_down_right_x(po_x, r):
    return po_x + 10 * math.sin(math.radians(r)) + 5 * math.cos(math.radians(r))


def S2W_down_right_y(po_y, r):
    return po_y + 10 * math.cos(math.radians(r))

# Turning from West to North
def W2N_up_left_x(po_x):
    return po_x


def W2N_up_left_y(po_y, r):
    return po_y - 10 * math.sin(math.radians(r))


def W2N_up_right_x(po_x, r):
    return po_x + 10 * math.cos(math.radians(r)) + 5 * math.sin(math.radians(r))


def W2N_up_right_y(po_y, r):
    return po_y - 10 * math.sin(math.radians(r))


def W2N_down_left_x(po_x):
    return po_x


def W2N_down_left_y(po_y, r):
    return po_y + 5 * math.sin(math.radians(r))


def W2N_down_right_x(po_x, r):
    return po_x + 10 * math.cos(math.radians(r)) + 5 * math.sin(math.radians(r))


def W2N_down_right_y(po_y, r):
    return po_y + 5 * math.cos(math.radians(r))