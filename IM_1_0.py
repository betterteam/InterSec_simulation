# coding:utf-8
# Test Intersection Manager with UDP
# Get vehicle proposal, return the result
# Starting of installing the collision detect algorithm

import sys
from datetime import datetime
import socket
import struct
import json
sys.path.append('Users/better/PycharmProjects/GUI_Qt5/Intersection')
import funcs
import math
import copy

# preparation as a server
server_address = ('localhost', 6789)
max_size = 4096
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(server_address)

STOP_CHAT = True

# load vehicle info
f = open('IM_00.json', 'r')
sendData = json.load(f)
f.close()

# Initiate intersection grid
grid = {}
intersec_grid = []
check_grid = []
t_ahead = 35

for i in range(270, 330, 10):
    for j in range(270, 330, 10):
        grid[(i, j)] = True

# whole time step that IM will predict in current time_step
for i in range(t_ahead):
    intersec_grid.append(copy.deepcopy(grid))

print(intersec_grid)

# Initiate veh rotating angle
veh_num = 10
r = []
for i in range(veh_num):
    r.append(0)

# Initiate bezier curve parameter
beze_t = []
up_left_x = []
up_left_y = []
down_left_x = []
down_left_y = []
up_right_x = []
up_right_y = []
down_right_x = []
down_right_y = []
for i in range(veh_num):
    beze_t.append(0)
    up_left_x.append(0)
    up_left_y.append(0)
    down_left_x.append(0)
    down_left_y.append(0)
    up_right_x.append(0)
    up_right_y.append(0)
    down_right_x.append(0)
    down_right_y.append(0)


print(intersec_grid[1])
print(intersec_grid[2])

print(intersec_grid[1])
print(intersec_grid[2])


def sendResult():
    while STOP_CHAT:
        check = 0

        print('starting the server at', datetime.now())
        print('waiting for a client to call.')

        data, client = server.recvfrom(max_size)

        data = data.decode('utf-8')
        recData = json.loads(data)

        print(recData["arrival_time"])

        if recData["arrival_time"] < 5:
            sendData[recData["Veh_id"]]["result"] = 1

        print(sendData)

        # Send Json
        mes = bytes(json.dumps(sendData[recData["Veh_id"]]), encoding='utf-8')
        server.sendto(mes, client)

    server.close()

# vehicles travel from W_1 to S_6
# origin and destination is a pattern of (x,y)
def light_veh_pattern1(veh_num, current, origin, destination, speed, time):
    new_position = current
    time = 0

    # Before veh get out of the intersection
    while new_position[1] <= destination[1]:

        # Check if all parts of veh have been in intersection
        if new_position[0] + speed < origin[0]:
            if not intersec_grid[time][(270, 270)]:
                break
            else:
                new_position = (new_position[0] + speed, new_position[1])
                intersec_grid[time][(270, 270)] = False
        else:
            # Calculate rotation angle
            if (((new_position[1] - 270 + speed) / 60) * 90 > 15):
                r[veh_num] = ((new_position[1] - 270 + 3) / 60) * 90
            else:
                r[veh_num] = 0

            # Calculate trajectory by using Bezier Curve
            x = pow(1 - (beze_t[veh_num] / 60), 2) * 270 + 2 * (beze_t[veh_num] / 60) * (
                1 - beze_t[veh_num] / 60) * 330 + pow(
                beze_t[veh_num] / 60, 2) * 330
            y = pow(1 - (beze_t[veh_num] / 60), 2) * 273 + 2 * (beze_t[veh_num] / 60) * (
                1 - beze_t[veh_num] / 60) * 273 + pow(
                beze_t[veh_num] / 60, 2) * 330

            beze_t[veh_num] += 2
            new_position = (x, y)

            # Calculate the big Square's coordinate
            up_left_x[veh_num] = funcs.coordinate_up_left_x(new_position[0], r[veh_num])
            up_left_y[veh_num] = funcs.coordinate_up_left_y(new_position[1])
            down_left_x[veh_num] = funcs.coordinate_down_left_x(new_position[0], r[veh_num])
            down_left_y[veh_num] = funcs.coordinate_down_left_y(new_position[1], r[veh_num])
            up_right_x[veh_num] = funcs.coordinate_up_right_x(new_position[0], r[veh_num])
            up_right_y[veh_num] = funcs.coordinate_up_right_y(new_position[1])
            down_right_x[veh_num] = funcs.coordinate_down_right_x(new_position[0], r[veh_num])
            down_right_y[veh_num] = funcs.coordinate_down_right_y(new_position[1], r[veh_num])

            # Up left
            if (up_left_x[veh_num] // 10 * 10, up_left_y[veh_num] // 10 * 10) in intersec_grid[time]:
                if intersec_grid[time][(up_left_x[veh_num] // 10 * 10, up_left_y[veh_num] // 10 * 10)] == False:
                    return False
                else:
                    intersec_grid[time][(up_left_x[veh_num] // 10 * 10, up_left_y[veh_num] // 10 * 10)] = False
                    check_grid.append((up_left_x[veh_num] // 10 * 10, up_left_y[veh_num] // 10 * 10))
                    # print(time)
                    # print(new_position)
                    # print((up_left_x[veh_num] // 10 * 10, up_left_y[veh_num] // 10 * 10))
                    # print('success')

            # Up right
            if ((up_right_x[veh_num]) // 10 * 10, up_right_y[veh_num] // 10 * 10) in intersec_grid[time]:
                if intersec_grid[time][((up_right_x[veh_num]) // 10 * 10, up_right_y[veh_num] // 10 * 10)] == False:
                    if ((up_right_x[veh_num]) // 10 * 10, up_right_y[veh_num] // 10 * 10) not in check_grid:
                        return False
                    else:
                        intersec_grid[time][((up_right_x[veh_num]) // 10 * 10, up_right_y[veh_num] // 10 * 10)] = False
                        check_grid.append(((up_right_x[veh_num]) // 10 * 10, up_right_y[veh_num] // 10 * 10))
                else:
                    intersec_grid[time][((up_right_x[veh_num]) // 10 * 10, up_right_y[veh_num] // 10 * 10)] = False
                    check_grid.append(((up_right_x[veh_num]) // 10 * 10, up_right_y[veh_num] // 10 * 10))
                    # print(time)
                    # print(new_position)
                    # print((up_left_x[veh_num] // 10 * 10, up_left_y[veh_num] // 10 * 10))
                    # print('success')

            # Down left
            if (down_left_x[veh_num] // 10 * 10, (down_left_y[veh_num]) // 10 * 10) in intersec_grid[time]:
                if intersec_grid[time][(down_left_x[veh_num] // 10 * 10, (down_left_y[veh_num]) // 10 * 10)] == False:
                    if (down_left_x[veh_num] // 10 * 10, (down_left_y[veh_num]) // 10 * 10) not in check_grid:
                        return False
                    else:
                        intersec_grid[time][(down_left_x[veh_num] // 10 * 10, (down_left_y[veh_num]) // 10 * 10)] = False
                        check_grid.append((down_left_x[veh_num] // 10 * 10, (down_left_y[veh_num]) // 10 * 10))
                else:
                    intersec_grid[time][(down_left_x[veh_num] // 10 * 10, (down_left_y[veh_num]) // 10 * 10)] = False
                    check_grid.append((down_left_x[veh_num] // 10 * 10, (down_left_y[veh_num]) // 10 * 10))
                    # print(time)
                    # print(new_position)
                    # print((up_left_x[veh_num] // 10 * 10, up_left_y[veh_num] // 10 * 10))
                    # print('success')

            # Down right
            if ((down_right_x[veh_num]) // 10 * 10, (down_right_y[veh_num]) // 10 * 10) in intersec_grid[time]:
                if intersec_grid[time][((down_right_x[veh_num]) // 10 * 10, (down_right_y[veh_num]) // 10 * 10)] == False:
                    if ((down_right_x[veh_num]) // 10 * 10, (down_right_y[veh_num]) // 10 * 10) not in check_grid:
                        return False
                    else:
                        intersec_grid[time][((down_right_x[veh_num]) // 10 * 10, (down_right_y[veh_num]) // 10 * 10)] = False
                else:
                    intersec_grid[time][((down_right_x[veh_num]) // 10 * 10, (down_right_y[veh_num]) // 10 * 10)] = False
                    # print(time)
                    # print(new_position)
                    # print((up_left_x[veh_num] // 10 * 10, up_left_y[veh_num] // 10 * 10))
                    # print('success')

        check_grid = []
        time += 1

        # if time > 8:
        #     break

    print(time)
    if time == 35:
        for i in range(t_ahead):
            print(intersec_grid[i])

    # Initiate intersection grid
    for i in range(t_ahead):
        for i in range(270, 330, 10):
            for j in range(270, 330, 10):
                grid[(i, j)] = True

    return True






def test_collision():
    print()

print(light_veh_pattern1(1, (262, 273), (270, 273), (330, 330), 2, 0))

#sendResult()