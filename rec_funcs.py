# coding:utf-8
# Functions that could be used to calculate the big rectangle
# Used From IM_2_2; veh_2_2

import math

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