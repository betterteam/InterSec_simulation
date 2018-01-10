# coding:utf-8
# From 180103
# add function check_lighten()

import sys
from datetime import datetime
import socket
import json

sys.path.append('Users/better/PycharmProjects/GUI_Qt5/Intersection_Ex')
import rec_funcs
import copy
import new_Rect


class IM():
    def __init__(self):
        # preparation as a server
        self.server_address = ('localhost', 6792)
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
        self.t_ahead = 35

        for i in range(600, 660, 10):
            for j in range(600, 660, 10):
                self.grid[(i, j)] = True

        # whole time step that IM will predict in current time_step
        for i in range(self.t_ahead + 1):
            self.intersec_grid.append(copy.deepcopy(self.grid))

        # Initiate veh rotating angle
        self.veh_num = 70
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

            # print(recData)

            veh_id = recData["Veh_id"]
            current = tuple(recData["current_position"])
            origin = tuple(recData["origin_4"])
            destination = tuple(recData["destination_4"])
            speed = recData["speed"]
            current_time = recData["time_step"]
            pattern = recData["pattern"]

            if pattern == 11:
                if self.light_veh_pattern11(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            elif pattern == 12:
                if self.light_veh_pattern12(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            elif pattern == 13:
                if self.light_veh_pattern13(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            elif pattern == 14:
                if self.light_veh_pattern14(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            elif pattern == 21:
                if self.light_veh_pattern21(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            elif pattern == 22:
                if self.light_veh_pattern22(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            elif pattern == 23:
                if self.light_veh_pattern23(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            elif pattern == 24:
                if self.light_veh_pattern24(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            elif pattern == 31:
                if self.light_veh_pattern31(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            elif pattern == 32:
                if self.light_veh_pattern32(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            elif pattern == 33:
                if self.light_veh_pattern33(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            else:
                if self.light_veh_pattern34(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            # Send Json
            mes = bytes(json.dumps(self.sendData[recData["Veh_id"]]), encoding='utf-8')
            self.server.sendto(mes, client)

        self.server.close()

    # function to Initiate intersection grid
    def init_intersec_grid(self, t_ahead):
        for k in range(t_ahead):
            for i in range(600, 660, 10):
                for j in range(600, 660, 10):
                    self.intersec_grid[k][(i, j)] = True

    # function to update intersection grid
    def update_intersec_grid(self, current_time, current_time_step, veh_num):
        sa = current_time - current_time_step

        self.time_step = current_time

        for i in range(sa):
            self.intersec_grid.append(copy.deepcopy(self.grid))
            del self.intersec_grid[0]

        self.r[veh_num] = 0

    #  check whether grid has already been lighten up
    def collision(self, veh_num, x, y, time):
        if (x // 10 * 10, y // 10 * 10) in self.intersec_grid[time]:
            if self.intersec_grid[time][(x // 10 * 10, y // 10 * 10)] == False:
                self.beze_t[veh_num] = 2
                return False
            else:
                return True
        else:
            return True

    def check_lighten(self, veh_num, up_left_x, up_left_y, up_right_x, up_right_y, down_left_x, down_left_y, down_right_x, down_right_y, time):
        # Up left
        if not self.collision(veh_num, up_left_x, up_left_y, time):
            print("upleft, pattern2", veh_num)
            return False

        # Up right
        if not self.collision(veh_num, up_right_x, up_right_y, time):
            print("upright, pattern2", veh_num)
            return False

        # Down left
        if not self.collision(veh_num, down_left_x, down_left_y, time):
            print("downleft, pattern2", veh_num)
            return False

        # Down right
        if ((down_right_x) // 10 * 10, (down_right_y) // 10 * 10) in \
                self.intersec_grid[time]:
            if self.intersec_grid[time][(down_right_x // 10 * 10,
                                         down_right_y // 10 * 10)] == False:
                print("downright, pattern2", veh_num)
                self.beze_t[veh_num] = 2
                return False
            # lighten up all four points together
            else:
                if (up_left_x // 10 * 10, up_left_y // 10 * 10) in self.intersec_grid[time]:
                    self.intersec_grid[time][
                        (up_left_x // 10 * 10, up_left_y // 10 * 10)] = False
                if (up_right_x // 10 * 10, up_right_y // 10 * 10) in self.intersec_grid[
                    time]:
                    self.intersec_grid[time][
                        (up_right_x // 10 * 10, up_right_y // 10 * 10)] = False
                if (down_left_x // 10 * 10, down_left_y // 10 * 10) in self.intersec_grid[
                    time]:
                    self.intersec_grid[time][
                        (down_left_x // 10 * 10, down_left_y // 10 * 10)] = False
                if (down_right_x // 10 * 10, down_right_y // 10 * 10) in self.intersec_grid[
                    time]:
                    self.intersec_grid[time][(
                        down_right_x // 10 * 10, down_right_y // 10 * 10)] = False
        # lighten up all three points together
        else:
            if (up_left_x // 10 * 10, up_left_y // 10 * 10) in self.intersec_grid[
                time]:
                self.intersec_grid[time][
                    (up_left_x // 10 * 10, up_left_y // 10 * 10)] = False
            if (up_right_x // 10 * 10, up_right_y // 10 * 10) in \
                    self.intersec_grid[time]:
                self.intersec_grid[time][
                    (up_right_x // 10 * 10, up_right_y // 10 * 10)] = False
            if (down_left_x // 10 * 10, down_left_y // 10 * 10) in \
                    self.intersec_grid[time]:
                self.intersec_grid[time][
                    (down_left_x // 10 * 10, down_left_y // 10 * 10)] = False
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
                        ((self.up_left_x[veh_num] + 10) // 10 * 10,self.down_left_y[veh_num] // 10 * 10)] = False
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

        return True

    # vehicles travel from N_1 to W_6
    # origin and destination is a pattern of (x,y)
    def light_veh_pattern11(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0

        # To light up grid(270, 270)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern11')

        # Before veh get out of the intersection
        while new_position[1] < destination[1]:

            # Check if all parts of veh have been in intersection
            if new_position[1] == 594:
                if not self.intersec_grid[time][(640, 600)]:
                    print('firstgrid')
                    return False
                else:
                    new_position = (origin[0], origin[1])
                    check_first = True
                    # print("check p11 current_time", current_time)
                    # print('time', time)
                    # print(self.beze_t[veh_num])
                    # print('new_position', new_position)
                    # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
                    # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
                    # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
                    # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
                    # print(self.intersec_grid[time])
                    time += 1

            else:

                # Calculate trajectory by using Bezier Curve
                x = pow(1 - (self.beze_t[veh_num] / 50), 2) * origin[0] + 2 * (self.beze_t[veh_num] / 50) * (
                    1 - self.beze_t[veh_num] / 50) * origin[0] + pow(
                    self.beze_t[veh_num] / 50, 2) * destination[0]
                y = pow(1 - (self.beze_t[veh_num] / 50), 2) * origin[1] + 2 * (self.beze_t[veh_num] / 50) * (
                    1 - self.beze_t[veh_num] / 50) * destination[1] + pow(
                    self.beze_t[veh_num] / 50, 2) * destination[1]

                new_position = (x, y)

                self.beze_t[veh_num] += 2

                print(new_position[1])
                print(origin[1])
                print(-(new_position[1] - (origin[1] + speed)) / 50)
                # Calculate rotation angle
                if 15.0 < (-(origin[1] - (new_position[1] + speed)) / 50) * 90 <= 90.0:
                    self.r[veh_num] = (-(origin[1] - (new_position[1] + speed)) / 50) * 90
                elif (-(origin[1] - (new_position[1] + speed)) / 50) * 90 > 90:
                    self.r[veh_num] = 90
                else:
                    self.r[veh_num] = 0

                # Calculate the big Square's coordinate
                (self.up_left_x[veh_num], self.up_left_y[veh_num]) = new_Rect.new_t_rec(x, y, 0)[0]
                (self.down_left_x[veh_num], self.down_left_y[veh_num]) = new_Rect.new_t_rec(x, y, 0)[1]
                (self.up_right_x[veh_num], self.up_right_y[veh_num]) = new_Rect.new_t_rec(x, y, 0)[2]
                (self.down_right_x[veh_num], self.down_right_y[veh_num]) = new_Rect.new_t_rec(x, y, 0)[3]

                if not self.check_lighten(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num],
                                          self.up_right_x[veh_num], self.up_right_y[veh_num],
                                          self.down_left_x[veh_num], self.down_left_y[veh_num],
                                          self.down_right_x[veh_num], self.down_right_y[veh_num], time):
                    return False

                if check_first:
                    self.intersec_grid[time][(640, 600)] = False
                check_first = False

                # print("check p11 current_time", current_time)
                # print('time', time)
                # print(self.beze_t[veh_num])
                # print('new_position', new_position, 'r', self.r[veh_num])
                # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
                # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
                # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
                # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
                # print(self.intersec_grid[time])
                time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

    def light_veh_pattern12(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0

        # To light up grid(270, 270)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern12')

        # Before veh get out of the intersection
        while new_position[1] > destination[1]:
            # Check if all parts of veh have been in intersection
            if new_position[1] == 666:
                if not self.intersec_grid[time][(610, 650)]:
                    print('firstgrid')
                    return False
                else:
                    new_position = (origin[0], origin[1])
                    check_first = True
                    # print("check p12 current_time", current_time)
                    # print('time', time)
                    # print(self.beze_t[veh_num])
                    # print('new_position', new_position)
                    # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
                    # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
                    # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
                    # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
                    # print(self.intersec_grid[time])
                    time += 1

            else:

                # Calculate trajectory by using Bezier Curve
                x = pow(1 - (self.beze_t[veh_num] / 50), 2) * origin[0] + 2 * (self.beze_t[veh_num] / 50) * (
                    1 - self.beze_t[veh_num] / 50) * origin[0] + pow(
                    self.beze_t[veh_num] / 50, 2) * destination[0]
                y = pow(1 - (self.beze_t[veh_num] / 50), 2) * origin[1] + 2 * (self.beze_t[veh_num] / 50) * (
                    1 - self.beze_t[veh_num] / 50) * destination[1] + pow(
                    self.beze_t[veh_num] / 50, 2) * destination[1]

                new_position = (x, y)

                self.beze_t[veh_num] += 2

                # Calculate rotation angle
                if 15.0 < ((origin[1] - (new_position[1] + speed)) / 50) * 90 <= 90.0:
                    self.r[veh_num] = ((origin[1] - (new_position[1] + speed)) / 50) * 90
                elif ((origin[1] - (new_position[1] + speed)) / 50) * 90 > 90:
                    self.r[veh_num] = 90
                else:
                    self.r[veh_num] = 0

                # Calculate the big Square's coordinate
                (self.up_left_x[veh_num], self.up_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[0]
                (self.down_left_x[veh_num], self.down_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[1]
                (self.up_right_x[veh_num], self.up_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[2]
                (self.down_right_x[veh_num], self.down_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[3]

                if not self.check_lighten(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num],
                                          self.up_right_x[veh_num], self.up_right_y[veh_num],
                                          self.down_left_x[veh_num], self.down_left_y[veh_num],
                                          self.down_right_x[veh_num], self.down_right_y[veh_num], time):
                    return False

                if check_first:
                    self.intersec_grid[time][(610, 650)] = False
                check_first = False

                # print("check p12 current_time", current_time)
                # print('time', time)
                # print(self.beze_t[veh_num])
                # print('new_position', new_position, 'r', self.r[veh_num])
                # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
                # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
                # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
                # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
                # print(self.intersec_grid[time])
                time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

    # vehicles travel from W_1 to S_6
    # origin and destination is a pattern of (x,y)
    def light_veh_pattern13(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0

        # To light up grid(270, 270)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern13')

        # Before veh get out of the intersection
        while new_position[0] < destination[0]:

            # Check if all parts of veh have been in intersection
            if new_position[0] == 594:
                if not self.intersec_grid[time][(600, 610)]:
                    print('firstgrid')
                    return False
                else:
                    new_position = (origin[0], origin[1])
                    check_first = True
                    # print("check p13 current_time", current_time)
                    # print('time', time)
                    # print(self.beze_t[veh_num])
                    # print('new_position', new_position, 'r', self.r[veh_num])
                    # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
                    # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
                    # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
                    # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
                    # print(self.intersec_grid[time])
                    time += 1
            else:

                # Calculate trajectory by using Bezier Curve
                x = pow(1 - (self.beze_t[veh_num] / 50), 2) * origin[0] + 2 * (self.beze_t[veh_num] / 50) * (
                    1 - self.beze_t[veh_num] / 50) * destination[0] + pow(
                    self.beze_t[veh_num] / 50, 2) * destination[0]
                y = pow(1 - (self.beze_t[veh_num] / 50), 2) * origin[1] + 2 * (self.beze_t[veh_num] / 50) * (
                    1 - self.beze_t[veh_num] / 50) * origin[1] + pow(
                    self.beze_t[veh_num] / 50, 2) * destination[1]

                new_position = (x, y)

                self.beze_t[veh_num] += 2

                # Calculate rotation angle
                if 15.0 < (-(origin[0] - (new_position[0] + speed)) / 50) * 90 <= 90.0:
                    self.r[veh_num] = (-(origin[0] - (new_position[0] + speed)) / 50) * 90
                elif (-(origin[0] - (new_position[0] + speed)) / 50) * 90 > 90:
                    self.r[veh_num] = 90
                else:
                    self.r[veh_num] = 0

                # Calculate the big Square's coordinate
                (self.up_left_x[veh_num], self.up_left_y[veh_num]) = new_Rect.new_t_rec(x, y, 0)[0]
                (self.down_left_x[veh_num], self.down_left_y[veh_num]) = new_Rect.new_t_rec(x, y, 0)[1]
                (self.up_right_x[veh_num], self.up_right_y[veh_num]) = new_Rect.new_t_rec(x, y, 0)[2]
                (self.down_right_x[veh_num], self.down_right_y[veh_num]) = new_Rect.new_t_rec(x, y, 0)[3]

                if not self.check_lighten(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num],
                                          self.up_right_x[veh_num], self.up_right_y[veh_num],
                                          self.down_left_x[veh_num], self.down_left_y[veh_num],
                                          self.down_right_x[veh_num], self.down_right_y[veh_num], time):
                    return False

                if check_first:
                    self.intersec_grid[time][(600, 610)] = False
                check_first = False

                # print("check p13 current_time", current_time)
                # print('time', time)
                # print(self.beze_t[veh_num])
                # print('new_position', new_position, 'r', self.r[veh_num])
                # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
                # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
                # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
                # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
                # print(self.intersec_grid[time])
                time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

    # vehicles travel from E_5 to N_2
    # origin and destination is a pattern of (x,y)
    def light_veh_pattern14(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0

        # To light up grid(270, 270)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern14')

        # Before veh get out of the intersection
        while new_position[0] > destination[0]:

            # Check if all parts of veh have been in intersection
            if new_position[0] == 666:
                if not self.intersec_grid[time][(650, 640)]:
                    print('firstgrid')
                    return False
                else:
                    new_position = (origin[0], origin[1])
                    check_first = True
                    # print("check p14 current_time", current_time)
                    # print('time', time)
                    # print(self.beze_t[veh_num])
                    # print('new_position', new_position)
                    # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
                    # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
                    # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
                    # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
                    # print(self.intersec_grid[time])
                    time += 1
            else:

                # Calculate trajectory by using Bezier Curve
                x = pow(1 - (self.beze_t[veh_num] / 50), 2) * origin[0] + 2 * (self.beze_t[veh_num] / 50) * (
                    1 - self.beze_t[veh_num] / 50) * destination[0] + pow(
                    self.beze_t[veh_num] / 50, 2) * destination[0]
                y = pow(1 - (self.beze_t[veh_num] / 50), 2) * origin[1] + 2 * (self.beze_t[veh_num] / 50) * (
                    1 - self.beze_t[veh_num] / 50) * origin[1] + pow(
                    self.beze_t[veh_num] / 50, 2) * destination[1]

                new_position = (x, y)

                self.beze_t[veh_num] += 2

                # Calculate rotation angle
                if 15.0 < ((origin[0] - (new_position[0] + speed)) / 50) * 90 <= 90.0:
                    self.r[veh_num] = ((origin[0] - (new_position[0] + speed)) / 50) * 90
                elif ((origin[0] - (new_position[0] + speed)) / 50) * 90 > 90:
                    self.r[veh_num] = 90
                else:
                    self.r[veh_num] = 0

                # Calculate the big Square's coordinate
                (self.up_left_x[veh_num], self.up_left_y[veh_num]) = new_Rect.new_t_rec(x, y, 0)[0]
                (self.down_left_x[veh_num], self.down_left_y[veh_num]) = new_Rect.new_t_rec(x, y, 0)[1]
                (self.up_right_x[veh_num], self.up_right_y[veh_num]) = new_Rect.new_t_rec(x, y, 0)[2]
                (self.down_right_x[veh_num], self.down_right_y[veh_num]) = new_Rect.new_t_rec(x, y, 0)[3]

                if not self.check_lighten(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num],
                                          self.up_right_x[veh_num], self.up_right_y[veh_num],
                                          self.down_left_x[veh_num], self.down_left_y[veh_num],
                                          self.down_right_x[veh_num], self.down_right_y[veh_num], time):
                    return False

                if check_first:
                    self.intersec_grid[time][(650, 640)] = False
                check_first = False

                # print("check p14 current_time", current_time)
                # print('time', time)
                # print(self.beze_t[veh_num])
                # print('new_position', new_position, 'r', self.r[veh_num])
                # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
                # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
                # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
                # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
                # print(self.intersec_grid[time])
                time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

    # vehicles travel from N_5 to S_5
    # origin and destination is a pattern of (x,y)
    def light_veh_pattern21(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0

        # to light up grid(320, 300)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern21')

        # Before veh get out of the intersection
        while new_position[1] < destination[1]:

            # Calculate trajectory by using Bezier Curve
            x = new_position[0]
            y = new_position[1] + speed

            new_position = (x, y)

            # Calculate the big Square's coordinate
            (self.up_left_x[veh_num], self.up_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[0]
            (self.down_left_x[veh_num], self.down_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[1]
            (self.up_right_x[veh_num], self.up_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[2]
            (self.down_right_x[veh_num], self.down_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[3]

            if not self.check_lighten(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num], self.up_right_x[veh_num], self.up_right_y[veh_num],
                               self.down_left_x[veh_num], self.down_left_y[veh_num], self.down_right_x[veh_num], self.down_right_y[veh_num], time):
                return False

            print("check p21 current_time", current_time)
            # print(self.intersec_grid[time])
            # print('time', time)
            # print('veh_num', veh_num)
            # print(self.beze_t)
            # print(self.beze_t[veh_num])
            print('new_position', new_position)
            # print(self.intersec_grid[time])
            time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

    def light_veh_pattern22(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0

        # to light up grid(320, 300)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern22')

        # Before veh get out of the intersection
        while new_position[1] > destination[1]:

            # Calculate trajectory by using Bezier Curve
            x = new_position[0]
            y = new_position[1] + speed

            new_position = (x, y)

            # Calculate the big Square's coordinate
            (self.up_left_x[veh_num], self.up_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[0]
            (self.down_left_x[veh_num], self.down_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[1]
            (self.up_right_x[veh_num], self.up_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[2]
            (self.down_right_x[veh_num], self.down_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[3]

            if not self.check_lighten(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num], self.up_right_x[veh_num], self.up_right_y[veh_num],
                               self.down_left_x[veh_num], self.down_left_y[veh_num], self.down_right_x[veh_num], self.down_right_y[veh_num], time):
                return False

            # print("check p22 current_time", current_time)
            # print(self.intersec_grid[time])
            # print('time', time)
            # print('veh_num', veh_num)
            # print(self.beze_t)
            # print(self.beze_t[veh_num])
            # print('new_position', new_position)
            # print(self.intersec_grid[time])
            time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

    def light_veh_pattern23(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0

        # to light up grid(320, 300)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern22')

        # Before veh get out of the intersection
        while new_position[0] < destination[0]:

            # Calculate trajectory by using Bezier Curve
            x = new_position[0] + speed
            y = new_position[1]

            new_position = (x, y)

            # Calculate the big Square's coordinate
            (self.up_left_x[veh_num], self.up_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[0]
            (self.down_left_x[veh_num], self.down_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[1]
            (self.up_right_x[veh_num], self.up_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[2]
            (self.down_right_x[veh_num], self.down_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[3]

            if not self.check_lighten(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num], self.up_right_x[veh_num], self.up_right_y[veh_num],
                               self.down_left_x[veh_num], self.down_left_y[veh_num], self.down_right_x[veh_num], self.down_right_y[veh_num], time):
                return False

            # print("check p23 current_time", current_time)
            # print(self.intersec_grid[time])
            # print('time', time)
            # print('veh_num', veh_num)
            # print(self.beze_t)
            # print(self.beze_t[veh_num])
            # print('new_position', new_position)
            # print(self.intersec_grid[time])
            time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

    def light_veh_pattern24(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0

        # to light up grid(320, 300)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern22')

        # Before veh get out of the intersection
        while new_position[0] > destination[0]:

            # Calculate trajectory by using Bezier Curve
            x = new_position[0] + speed
            y = new_position[1]

            new_position = (x, y)

            # Calculate the big Square's coordinate
            (self.up_left_x[veh_num], self.up_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[0]
            (self.down_left_x[veh_num], self.down_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[1]
            (self.up_right_x[veh_num], self.up_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[2]
            (self.down_right_x[veh_num], self.down_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[3]

            if not self.check_lighten(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num], self.up_right_x[veh_num], self.up_right_y[veh_num],
                               self.down_left_x[veh_num], self.down_left_y[veh_num], self.down_right_x[veh_num], self.down_right_y[veh_num], time):
                return False

            # print("check p24 current_time", current_time)
            # print(self.intersec_grid[time])
            # print('time', time)
            # print('veh_num', veh_num)
            # print(self.beze_t)
            # print(self.beze_t[veh_num])
            # print('new_position', new_position)
            # print(self.intersec_grid[time])
            time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

    # vehicles travel from N_5 to E_2
    # origin and destination is a pattern of (x,y)
    def light_veh_pattern31(self, veh_num, current, origin, destination, speed, current_time):

        new_position = current
        time = 0

        # To light up grid(270, 270)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern31')

        # Before veh get out of the intersection
        while new_position[1] < destination[1]:
            if new_position[1] == 594:
                if not self.intersec_grid[time][(640, 600)]:
                    print('firstgrid')
                    return False
                else:
                    new_position = (origin[0], origin[1])
                    check_first = True
                    # print("check p31 current_time", current_time)
                    # print('time', time)
                    # print(self.beze_t[veh_num])
                    # print('new_position', new_position)
                    # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
                    # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
                    # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
                    # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
                    # print(self.intersec_grid[time])
                    time += 1
            else:
                # All parts of veh have been in intersection

                # Calculate trajectory by using Bezier Curve
                x = pow(1 - (self.beze_t[veh_num] / 20), 2) * origin[0] + 2 * (self.beze_t[veh_num] / 20) * (
                    1 - self.beze_t[veh_num] / 20) * origin[0] + pow(
                    self.beze_t[veh_num] / 20, 2) * destination[0]
                y = pow(1 - (self.beze_t[veh_num] / 20), 2) * origin[1] + 2 * (self.beze_t[veh_num] / 20) * (
                    1 - self.beze_t[veh_num] / 20) * destination[1] + pow(
                    self.beze_t[veh_num] / 20, 2) * destination[1]

                new_position = (x, y)

                # Calculate rotation angle
                if 15.0 < (-(origin[1] - (new_position[1] + speed)) / 20) * 90 <= 90.0:
                    self.r[veh_num] = -(-(origin[1] - (new_position[1] + speed)) / 20) * 90
                elif (-(origin[1] - (new_position[1] + speed)) / 20) * 90 > 90:
                    self.r[veh_num] = -90
                else:
                    self.r[veh_num] = 0

                self.beze_t[veh_num] += 2

                # Calculate the big Square's coordinate
                (self.up_left_x[veh_num], self.up_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[0]
                (self.down_left_x[veh_num], self.down_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[1]
                (self.up_right_x[veh_num], self.up_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[2]
                (self.down_right_x[veh_num], self.down_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[3]

                if not self.check_lighten(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num],
                                          self.up_right_x[veh_num], self.up_right_y[veh_num],
                                          self.down_left_x[veh_num], self.down_left_y[veh_num],
                                          self.down_right_x[veh_num], self.down_right_y[veh_num], time):
                    return False

            if check_first:
                self.intersec_grid[time][(640, 600)] = False
            check_first = False

            # print("check p31 current_time", current_time)
            # print('time', time)
            # print(self.beze_t[veh_num])
            # print('new_position', new_position, 'r:', self.r[veh_num])
            # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
            # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
            # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
            # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
            # print(self.intersec_grid[time])
            time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

    # vehicles travel from S_3 to W_4
    # origin and destination is a pattern of (x,y)
    def light_veh_pattern32(self, veh_num, current, origin, destination, speed, current_time):

        new_position = current
        time = 0

        # To light up grid(270, 270)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern32')

        # Before veh get out of the intersection
        while new_position[1] > destination[1]:
            if new_position[1] == 666:
                if not self.intersec_grid[time][(610, 650)]:
                    print('firstgrid')
                    return False
                else:
                    new_position = (origin[0], origin[1])
                    check_first = True
                    # print("check p32 current_time", current_time)
                    # print('time', time)
                    # print(self.beze_t[veh_num])
                    # print('new_position', new_position)
                    # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
                    # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
                    # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
                    # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
                    # print(self.intersec_grid[time])
                    time += 1
            else:
                # All parts of veh have been in intersection

                # Calculate trajectory by using Bezier Curve
                x = pow(1 - (self.beze_t[veh_num] / 20), 2) * origin[0] + 2 * (self.beze_t[veh_num] / 20) * (
                    1 - self.beze_t[veh_num] / 20) * origin[0] + pow(
                    self.beze_t[veh_num] / 20, 2) * destination[0]
                y = pow(1 - (self.beze_t[veh_num] / 20), 2) * origin[1] + 2 * (self.beze_t[veh_num] / 20) * (
                    1 - self.beze_t[veh_num] / 20) * destination[1] + pow(
                    self.beze_t[veh_num] / 20, 2) * destination[1]

                new_position = (x, y)

                # Calculate rotation angle
                if 15.0 < ((origin[1] - (new_position[1] + speed)) / 20) * 90 <= 90.0:
                    self.r[veh_num] = ((origin[1] - (new_position[1] + speed)) / 20) * 90
                elif ((origin[1] - (new_position[1] + speed)) / 20) * 90 > 90:
                    self.r[veh_num] = 90
                else:
                    self.r[veh_num] = 0

                self.beze_t[veh_num] += 2


                # Calculate the big Square's coordinate
                (self.up_left_x[veh_num], self.up_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[0]
                (self.down_left_x[veh_num], self.down_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[1]
                (self.up_right_x[veh_num], self.up_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[2]
                (self.down_right_x[veh_num], self.down_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[3]

                if not self.check_lighten(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num],
                                          self.up_right_x[veh_num], self.up_right_y[veh_num],
                                          self.down_left_x[veh_num], self.down_left_y[veh_num],
                                          self.down_right_x[veh_num], self.down_right_y[veh_num], time):
                    return False

            if check_first:
                self.intersec_grid[time][(610, 650)] = False
            check_first = False

            # print("check p32 current_time", current_time)
            # print('time', time)
            # print(self.beze_t[veh_num])
            # print('new_position', new_position, 'r:', self.r[veh_num])
            # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
            # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
            # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
            # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
            # print(self.intersec_grid[time])
            time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

    # vehicles travel from W_2 to N_2
    # origin and destination is a pattern of (x,y)
    def light_veh_pattern33(self, veh_num, current, origin, destination, speed, current_time):

        new_position = current
        time = 0

        # To light up grid(270, 270)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern33')

        # Before veh get out of the intersection
        while new_position[0] < destination[0]:
            if new_position[0] == 594:
                if not self.intersec_grid[time][(600, 610)]:
                    print('firstgrid')
                    return False
                else:
                    new_position = (origin[0], origin[1])
                    check_first = True
                    # print("check p33 current_time", current_time)
                    # print('time', time)
                    # print(self.beze_t[veh_num])
                    # print('new_position', new_position)
                    # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
                    # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
                    # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
                    # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
                    # print(self.intersec_grid[time])
                    time += 1
            else:
                # All parts of veh have been in intersection

                # Calculate trajectory by using Bezier Curve
                x = pow(1 - (self.beze_t[veh_num] / 20), 2) * origin[0] + 2 * (self.beze_t[veh_num] / 20) * (
                    1 - self.beze_t[veh_num] / 20) * destination[0] + pow(
                    self.beze_t[veh_num] / 20, 2) * destination[0]
                y = pow(1 - (self.beze_t[veh_num] / 20), 2) * origin[1] + 2 * (self.beze_t[veh_num] / 20) * (
                    1 - self.beze_t[veh_num] / 20) * origin[1] + pow(
                    self.beze_t[veh_num] / 20, 2) * destination[1]

                new_position = (x, y)

                # Calculate rotation angle
                if 15.0 < -((origin[0] - (new_position[0] + speed)) / 20) * 90 <= 90.0:
                    self.r[veh_num] = -(-((origin[0] - (new_position[0] + speed)) / 20)) * 90
                elif -((origin[0] - (new_position[0] + speed)) / 20) * 90 > 90:
                    self.r[veh_num] = -90
                else:
                    self.r[veh_num] = 0

                self.beze_t[veh_num] += 2


                # Calculate the big Square's coordinate
                (self.up_left_x[veh_num], self.up_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[0]
                (self.down_left_x[veh_num], self.down_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[1]
                (self.up_right_x[veh_num], self.up_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[2]
                (self.down_right_x[veh_num], self.down_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[3]

                if not self.check_lighten(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num],
                                          self.up_right_x[veh_num], self.up_right_y[veh_num],
                                          self.down_left_x[veh_num], self.down_left_y[veh_num],
                                          self.down_right_x[veh_num], self.down_right_y[veh_num], time):
                    return False

            if check_first:
                self.intersec_grid[time][(600, 610)] = False
            check_first = False

            # print("check p33 current_time", current_time)
            # print('time', time)
            # print(self.beze_t[veh_num])
            # print('new_position', new_position, 'r:', self.r[veh_num])
            # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
            # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
            # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
            # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
            # print(self.intersec_grid[time])
            time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

    # vehicles travel from E_5 to S_5
    # origin and destination is a pattern of (x,y)
    def light_veh_pattern34(self, veh_num, current, origin, destination, speed, current_time):

        new_position = current
        time = 0

        # To light up grid(270, 270)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern34')

        # Before veh get out of the intersection
        while new_position[0] > destination[0]:
            if new_position[0] == 666:
                if not self.intersec_grid[time][(650, 640)]:
                    print('firstgrid')
                    return False
                else:
                    new_position = (origin[0], origin[1])
                    check_first = True
                    # print("check p34 current_time", current_time)
                    # print('time', time)
                    # print(self.beze_t[veh_num])
                    # print('new_position', new_position)
                    # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
                    # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
                    # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
                    # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
                    # print(self.intersec_grid[time])
                    time += 1
            else:
                # All parts of veh have been in intersection

                # Calculate trajectory by using Bezier Curve
                x = pow(1 - (self.beze_t[veh_num] / 20), 2) * origin[0] + 2 * (self.beze_t[veh_num] / 20) * (
                    1 - self.beze_t[veh_num] / 20) * destination[0] + pow(
                    self.beze_t[veh_num] / 20, 2) * destination[0]
                y = pow(1 - (self.beze_t[veh_num] / 20), 2) * origin[1] + 2 * (self.beze_t[veh_num] / 20) * (
                    1 - self.beze_t[veh_num] / 20) * origin[1] + pow(
                    self.beze_t[veh_num] / 20, 2) * destination[1]

                # Calculate rotation angle
                if ((origin[0] - (new_position[0] + speed)) / 20) * 90 > 15:
                    self.r[veh_num] = -((origin[0] - (new_position[0] + speed)) / 20) * 90
                elif ((origin[0] - (new_position[0] + speed)) / 20) * 90 > 90:
                    self.r[veh_num] = -90
                else:
                    self.r[veh_num] = 0

                self.beze_t[veh_num] += 2
                new_position = (x, y)

                # Calculate the big Square's coordinate
                (self.up_left_x[veh_num], self.up_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[0]
                (self.down_left_x[veh_num], self.down_left_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[1]
                (self.up_right_x[veh_num], self.up_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[2]
                (self.down_right_x[veh_num], self.down_right_y[veh_num]) = new_Rect.new_v_rec(x, y, 0)[3]

                if not self.check_lighten(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num],
                                          self.up_right_x[veh_num], self.up_right_y[veh_num],
                                          self.down_left_x[veh_num], self.down_left_y[veh_num],
                                          self.down_right_x[veh_num], self.down_right_y[veh_num], time):
                    return False

            if check_first:
                self.intersec_grid[time][(650, 640)] = False
            check_first = False

            # print("check p34 current_time", current_time)
            # print('time', time)
            # print(self.beze_t[veh_num])
            # print('new_position', new_position, 'r', self.r[veh_num])
            # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
            # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
            # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
            # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
            # print(self.intersec_grid[time])
            time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

if __name__ == '__main__':
    test = IM().sendResult()
    # IM.sendResult()
    # sys.exit(test.exec_())