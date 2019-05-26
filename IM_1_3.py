# coding:utf-8
# Test Intersection Manager with UDP
# Get vehicle proposal, return the result
# Starting of installing the collision detect algorithm
# Unify into a class
# Add light_veh_pattern3
# Change IM's grid updating method

import sys
from datetime import datetime
import socket
import struct
import json
sys.path.append('Users/better/PycharmProjects/GUI_Qt5/Intersection')
import funcs
import math
import copy

class IM():
    def __init__(self):
        # preparation as a server
        self.server_address = ('localhost', 6789)
        self.max_size = 4096
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(self.server_address)

        self.STOP_CHAT = True

        # load vehicle info
        self.f = open('IM_00.json', 'r')
        self.sendData = json.load(self.f)
        self.f.close()

        # Initiate intersection grid
        self.grid = {}
        self.intersec_grid = []
        self.check_grid = []
        self.t_ahead = 34

        for i in range(270, 330, 10):
            for j in range(270, 330, 10):
                self.grid[(i, j)] = True

        # whole time step that IM will predict in current time_step
        for i in range(self.t_ahead + 1):
            self.intersec_grid.append(copy.deepcopy(self.grid))

        #print(self.intersec_grid)

        # Initiate veh rotating angle
        self.veh_num = 11
        self.r = []
        for i in range(self.veh_num):
            self.r.append(0)

        # Initiate bezier curve parameter
        self.beze_t = []
        self.up_left_x = []
        self.up_left_y = []
        self.down_left_x = []
        self.down_left_y = []
        self.up_right_x = []
        self.up_right_y = []
        self.down_right_x = []
        self.down_right_y = []
        for i in range(self.veh_num):
            self.beze_t.append(2)
            self.up_left_x.append(0)
            self.up_left_y.append(0)
            self.down_left_x.append(0)
            self.down_left_y.append(0)
            self.up_right_x.append(0)
            self.up_right_y.append(0)
            self.down_right_x.append(0)
            self.down_right_y.append(0)

        # Initiate time step
        self.time_step = 0

    def sendResult(self):
        while self.STOP_CHAT:
            self.check = 0

            print('starting the server at', datetime.now())
            print('waiting for a client to call.')

            data, client = self.server.recvfrom(self.max_size)

            data = data.decode('utf-8')
            recData = json.loads(data)

            veh_id = recData["Veh_id"]
            current = tuple(recData["current_position"])
            origin = tuple(recData["origin"])
            destination = tuple(recData["destination"])
            speed = recData["speed"]
            current_time = recData["time_step"]
            pattern = recData["pattern"]

            if pattern == 1:
                if self.light_veh_pattern1(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            else:
                if self.light_veh_pattern3(veh_id, current, origin, destination, speed, current_time):
                    # print("self.sendData", self.sendData)
                    # print("recData:", recData)
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            # Send Json
            mes = bytes(json.dumps(self.sendData[recData["Veh_id"]]), encoding='utf-8')
            self.server.sendto(mes, client)

        self.server.close()

    # vehicles travel from W_1 to S_6
    # origin and destination is a pattern of (x,y)
    def light_veh_pattern1(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0
        # Avoid situation that grid is lighted up by same vehicle
        check_grid = []
        # To light up grid(270, 270)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            for k in range(self.t_ahead):
                for i in range(270, 330, 10):
                    for j in range(270, 330, 10):
                        self.intersec_grid[k][(i, j)] = True

        if current_time > self.time_step:
            sa = current_time - self.time_step
            print('sa', sa)
            self.time_step = current_time

            # Update intersec_grid for right times
            for i in range(sa):
                self.intersec_grid.append(copy.deepcopy(self.grid))
                del self.intersec_grid[0]
            print('Pattern1')

            for i in range(veh_num):
                self.r[i] = 0
            # print(self.time_step)
            # print(self.intersec_grid[0])
            # print(self.intersec_grid[36])

        # Before veh get out of the intersection
        while new_position[1] < destination[1]:

            # Check if all parts of veh have been in intersection
            if new_position[0] + speed <= origin[0]:
                if not self.intersec_grid[time][(270, 270)]:
                    print('firstgrid')
                    return False
                else:
                    new_position = (new_position[0] + speed, new_position[1])
                    check_first = True
                    # self.intersec_grid[time][(270, 270)] = False
            else:
                # All parts of veh have been in intersection
                # Calculate rotation angle
                if (((new_position[1] - 270 + speed) / 60) * 90 > 15):
                    self.r[veh_num] = ((new_position[1] - 270 + 3) / 60) * 90
                else:
                    self.r[veh_num] = 0

                if (((new_position[1] - 270 + speed) / 60) * 90 > 90):
                    self.r[veh_num] = 90


                # Calculate trajectory by using Bezier Curve
                x = pow(1 - (self.beze_t[veh_num] / 60), 2) * 270 + 2 * (self.beze_t[veh_num] / 60) * (
                    1 - self.beze_t[veh_num] / 60) * 330 + pow(
                    self.beze_t[veh_num] / 60, 2) * 330
                y = pow(1 - (self.beze_t[veh_num] / 60), 2) * 273 + 2 * (self.beze_t[veh_num] / 60) * (
                    1 - self.beze_t[veh_num] / 60) * 273 + pow(
                    self.beze_t[veh_num] / 60, 2) * 330

                self.beze_t[veh_num] += 2
                new_position = (x, y)

                # Calculate the big Square's coordinate
                self.up_left_x[veh_num] = funcs.coordinate_up_left_x(new_position[0], self.r[veh_num])
                self.up_left_y[veh_num] = funcs.coordinate_up_left_y(new_position[1])
                self.down_left_x[veh_num] = funcs.coordinate_down_left_x(new_position[0], self.r[veh_num])
                self.down_left_y[veh_num] = funcs.coordinate_down_left_y(new_position[1], self.r[veh_num])
                self.up_right_x[veh_num] = funcs.coordinate_up_right_x(new_position[0], self.r[veh_num])
                self.up_right_y[veh_num] = funcs.coordinate_up_right_y(new_position[1])
                self.down_right_x[veh_num] = funcs.coordinate_down_right_x(new_position[0], self.r[veh_num])
                self.down_right_y[veh_num] = funcs.coordinate_down_right_y(new_position[1], self.r[veh_num])

                # Up left
                # print(time)
                if (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10) in self.intersec_grid[time]:
                    if self.intersec_grid[time][(self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] == False:
                        print('upleft')
                        self.beze_t[veh_num] = 2
                        return False
                    else:
                        # self.intersec_grid[time][(self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                        check_grid.append((self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10))

                # Up right
                if ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10) in self.intersec_grid[time]:
                    if self.intersec_grid[time][((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] == False:
                        if ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10) not in check_grid:
                            print('upright')
                            self.beze_t[veh_num] = 2
                            return False
                        # else:
                        #     self.intersec_grid[time][((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                        #     check_grid.append(((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10))
                    else:
                        # self.intersec_grid[time][((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                        check_grid.append(((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10))

                # Down left
                if (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10) in self.intersec_grid[time]:
                    if self.intersec_grid[time][(self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] == False:
                        if (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10) not in check_grid:
                            print('Downleft')
                            self.beze_t[veh_num] = 2
                            return False
                        # else:
                        #     self.intersec_grid[time][(self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                        #     check_grid.append((self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10))
                    else:
                        # self.intersec_grid[time][(self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                        check_grid.append((self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10))

                # Down right
                if ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10) in self.intersec_grid[time]:
                    if self.intersec_grid[time][((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] == False:
                        if ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10) not in check_grid:
                            print('downright')
                            self.beze_t[veh_num] = 2
                            return False
                        # else:
                        #     self.intersec_grid[time][((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] = False
                    else:
                        self.intersec_grid[time][
                            (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                        self.intersec_grid[time][
                            ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                        self.intersec_grid[time][
                            (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                        self.intersec_grid[time][((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] = False
                # Situation that down_right is out of the region of inter_sec grid
                else:
                    if (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10) in self.intersec_grid[time]:
                        self.intersec_grid[time][
                            (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                    if ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10) in self.intersec_grid[time]:
                        self.intersec_grid[time][
                            ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                    if (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10) in self.intersec_grid[time]:
                        self.intersec_grid[time][
                            (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                    # situation that middle grid exists
                    # x coordinate is the reason
                    if abs(self.up_left_x[veh_num] - self.up_right_x[veh_num]) > 10:
                        if ((self.up_left_x[veh_num] + 10) // 10 * 10, self.up_left_y[veh_num] // 10 * 10) in \
                                self.intersec_grid[time]:
                            self.intersec_grid[time][
                                ((self.up_left_x[veh_num] + 10) // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                        if ((self.up_left_x[veh_num] + 10) // 10 * 10, self.down_left_y[veh_num] // 10 * 10) in \
                                self.intersec_grid[time]:
                            self.intersec_grid[time][
                                ((self.up_left_x[veh_num] + 10) // 10 * 10, self.down_left_y[veh_num] // 10 * 10)] = False
                    # y coordinate is the reason
                    if abs(self.up_left_y[veh_num] - self.down_left_y[veh_num]) > 10:
                        if (self.up_left_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10) in \
                                self.intersec_grid[time]:
                            self.intersec_grid[time][
                                (self.up_left_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10)] = False
                        if (self.up_right_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10) in \
                                self.intersec_grid[time]:
                            self.intersec_grid[time][
                                (self.up_right_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10)] = False

            if check_first:
                self.intersec_grid[time][(270, 270)] = False
            check_first = False

            print("check p1 current_time", current_time)
            #print(self.intersec_grid[time])
            check_grid = []
            print('time', time)
            print('veh_num', veh_num)
            print(self.beze_t[veh_num])
            print('new_position', new_position, 'r', self.r)
            print(self.intersec_grid[time])
            # if time == 30:
            #     print((self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10))
            #     print(((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10))
            #     print((self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10))
            #     print(((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10))
            time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

    # vehicles travel from E_5 to W_5
    # origin and destination is a pattern of (x,y)
    def light_veh_pattern3(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0
        # Avoid situation that grid is lighted up by same vehicle
        check_grid = []
        # to light up grid(320, 300)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            for k in range(self.t_ahead):
                for i in range(270, 330, 10):
                    for j in range(270, 330, 10):
                        self.intersec_grid[k][(i, j)] = True

        if current_time > self.time_step:
            sa = current_time - self.time_step
            print('sa', sa)
            self.time_step = current_time

            # Upgrade intersec_gird for right times
            for i in range(sa):
                self.intersec_grid.append(copy.deepcopy(self.grid))
                del self.intersec_grid[0]
            print('Pattern3')
            # print(self.time_step)
            # print(self.intersec_grid[0])
            # print(self.intersec_grid[36])

        # Before veh get out of the intersection
        while new_position[0] >= destination[0]:

            # Check if all parts of veh have been in intersection
            if new_position[0] - speed < origin[0]:
                if not self.intersec_grid[time][(320, 300)]:
                    print("first grid, pattern3")
                    return False
                else:
                    new_position = (new_position[0] - speed, new_position[1])
                    check_first = True
                    # self.intersec_grid[time][(320, 300)] = False
            else:

                # Calculate trajectory by using Bezier Curve
                x = new_position[0] - speed
                y = new_position[1]

                new_position = (x, y)

                # Calculate the big Square's coordinate
                self.up_left_x[veh_num] = new_position[0]
                self.up_left_y[veh_num] = new_position[1]
                self.down_left_x[veh_num] = new_position[0]
                self.down_left_y[veh_num] = new_position[1] + 5
                self.up_right_x[veh_num] = new_position[0] + 10
                self.up_right_y[veh_num] = new_position[1]
                self.down_right_x[veh_num] = new_position[0] + 10
                self.down_right_y[veh_num] = new_position[1] + 5

                # Up left
                if (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10) in self.intersec_grid[
                    time]:
                    if self.intersec_grid[time][
                        (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] == False:
                        print("upleft, pattern3")
                        return False
                    else:
                        # self.intersec_grid[time][
                        #     (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                        check_grid.append((self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10))

                # Up right
                if ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10) in \
                        self.intersec_grid[time]:
                    if self.intersec_grid[time][
                        ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] == False:
                        if ((self.up_right_x[veh_num]) // 10 * 10,
                            self.up_right_y[veh_num] // 10 * 10) not in check_grid:
                            print("upright, pattern3")
                            return False
                        # else:
                            # self.intersec_grid[time][(
                            # (self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                            # check_grid.append(
                            #     ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10))
                    else:
                        # self.intersec_grid[time][
                        #     ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                        check_grid.append(
                            ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10))

                # Down left
                if (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10) in \
                        self.intersec_grid[time]:
                    if self.intersec_grid[time][
                        (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] == False:
                        if (self.down_left_x[veh_num] // 10 * 10,
                            (self.down_left_y[veh_num]) // 10 * 10) not in check_grid:
                            print("downleft, pattern3")
                            return False
                        # else:
                        #     self.intersec_grid[time][(
                        #     self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                        #     check_grid.append(
                        #         (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10))
                    else:
                        # self.intersec_grid[time][
                        #     (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                        check_grid.append(
                            (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10))

                # Down right
                if ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10) in \
                        self.intersec_grid[time]:
                    if self.intersec_grid[time][((self.down_right_x[veh_num]) // 10 * 10,
                                                 (self.down_right_y[veh_num]) // 10 * 10)] == False:
                        if ((self.down_right_x[veh_num]) // 10 * 10,
                            (self.down_right_y[veh_num]) // 10 * 10) not in check_grid:
                            print("downright, pattern3")
                            return False
                        # else:
                        #     self.intersec_grid[time][((self.down_right_x[veh_num]) // 10 * 10,
                        #                               (self.down_right_y[veh_num]) // 10 * 10)] = False
                    else:
                        self.intersec_grid[time][
                            (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                        self.intersec_grid[time][
                            ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                        self.intersec_grid[time][
                            (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                        self.intersec_grid[time][(
                        (self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] = False

            if check_first:
                self.intersec_grid[time][(320, 300)] = False
            check_first = False

            print("check p3 current_time", current_time)
            # print(self.intersec_grid[time])
            check_grid = []
            print('time', time)
            print(self.beze_t[veh_num])
            print('new_position', new_position, 'r', self.r)
            print(self.intersec_grid[time])
            time += 1

        return True

if __name__ == '__main__':
    test = IM().sendResult()
    #IM.sendResult()
    #sys.exit(test.exec_())