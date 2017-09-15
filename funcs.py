# coding:utf-8
# functions that could be used to calculate

import math

def coordinate_up_left_x(po_x, r):
    return po_x - 5 * math.cos(math.radians(r))


def coordinate_up_left_y(po_y):
    return po_y


def coordinate_up_right_x(po_x, r):
    return po_x + 10 * math.cos(math.radians(r))


def coordinate_up_right_y(po_y):
    return po_y


def coordinate_down_left_x(po_x, r):
    return po_x - 5 * math.cos(math.radians(r))


def coordinate_down_left_y(po_y, r):
    return po_y + 5 * math.sin(math.radians(r)) + 10 * math.cos(math.radians(r))


def coordinate_down_right_x(po_x, r):
    return po_x + 10 * math.cos(math.radians(r))


def coordinate_down_right_y(po_y, r):
    return po_y + 10 * math.sin(math.radians(r)) + 5 * math.cos(math.radians(r))