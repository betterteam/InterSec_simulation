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
def new_v_rec(c_x, c_y, r):
    up_left = (c_x - 5 / 2, c_y - 10 / 2)
    up_right = (c_x + 5 / 2, c_y - 10 / 2)
    down_left = (c_x - 5 / 2, c_y + 10 / 2)
    down_right = (c_x + 5 / 2, c_y + 10 / 2)

    new_up_left = new_rec(c_x, c_y, up_left[0], up_left[1], r)
    new_up_right = new_rec(c_x, c_y, up_right[0], up_right[1], r)
    new_down_left = new_rec(c_x, c_y, down_left[0], down_left[1], r)
    new_down_right = new_rec(c_x, c_y, down_right[0], down_right[1], r)

    # qp.drawLine(new_up_left[0], new_up_left[1], new_up_right[0], new_up_right[1])
    # qp.drawLine(new_up_left[0], new_up_left[1], new_down_left[0], new_down_left[1])
    # qp.drawLine(new_up_right[0], new_up_right[1], new_down_right[0], new_down_right[1])
    # qp.drawLine(new_down_left[0], new_down_left[1], new_down_right[0], new_down_right[1])
    return new_up_left, new_up_right, new_down_left, new_down_right


# begin as a tropical rectangle
# center_x position, center_y position and rotation angle
def new_t_rec(c_x, c_y, r):
    up_left = (c_x - 10 / 2, c_y - 5 / 2)
    up_right = (c_x + 10 / 2, c_y - 5 / 2)
    down_left = (c_x - 10 / 2, c_y + 5 / 2)
    down_right = (c_x + 10 / 2, c_y + 5 / 2)

    new_up_left = new_rec(c_x, c_y, up_left[0], up_left[1], r)
    new_up_right = new_rec(c_x, c_y, up_right[0], up_right[1], r)
    new_down_left = new_rec(c_x, c_y, down_left[0], down_left[1], r)
    new_down_right = new_rec(c_x, c_y, down_right[0], down_right[1], r)

    # qp.drawLine(new_up_left[0], new_up_left[1], new_up_right[0], new_up_right[1])
    # qp.drawLine(new_up_left[0], new_up_left[1], new_down_left[0], new_down_left[1])
    # qp.drawLine(new_up_right[0], new_up_right[1], new_down_right[0], new_down_right[1])
    # qp.drawLine(new_down_left[0], new_down_left[1], new_down_right[0], new_down_right[1])
    return new_up_left, new_up_right, new_down_left, new_down_right

# print(new_v_rec(315, 265, 0))
# ((x, y), (x1, y1), (x2, y2), (x3, y3)) = new_v_rec(315, 265, 0)
# (x, y) = new_v_rec(315, 265, 0)[0]
# print(x)
# print(y)