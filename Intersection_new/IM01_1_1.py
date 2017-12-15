# coding:utf-8
# From 1213
# With two traffic lines

import sys
from datetime import datetime
import socket
import json

sys.path.append('Users/better/PycharmProjects/GUI_Qt5/Intersection')
import rec_funcs
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
        self.t_ahead = 35

        for i in range(270, 330, 10):
            for j in range(270, 330, 10):
                self.grid[(i, j)] = True

        # whole time step that IM will predict in current time_step
        for i in range(self.t_ahead + 1):
            self.intersec_grid.append(copy.deepcopy(self.grid))

        # Initiate veh rotating angle
        self.veh_num = 60
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

            print(recData)

            veh_id = recData["Veh_id"]
            current = tuple(recData["current_position"])
            origin = tuple(recData["origin_1"])
            destination = tuple(recData["destination_1"])
            speed = recData["speed"]
            current_time = recData["time_step"]
            pattern = recData["pattern"]

            if pattern == 1:
                if self.light_veh_pattern1(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            elif pattern == 2:
                if self.light_veh_pattern2(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            elif pattern == 3:
                if self.light_veh_pattern3(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            elif pattern == 5:
                if self.light_veh_pattern5(veh_id, current, origin, destination, speed, current_time):
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    self.sendData[recData["Veh_id"]]["result"] = 0

            else:
                if self.light_veh_pattern4(veh_id, current, origin, destination, speed, current_time):
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
            for i in range(270, 330, 10):
                for j in range(270, 330, 10):
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

    # vehicles travel from W_1 to S_6
    # origin and destination is a pattern of (x,y)
    def light_veh_pattern1(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0

        # To light up grid(270, 270)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern1')

        # Before veh get out of the intersection
        while new_position[1] < destination[1]:

            # Check if all parts of veh have been in intersection
            if new_position[0] + speed <= origin[0] + 2:
                if not self.intersec_grid[time][(270, 280)]:
                    print('firstgrid')
                    return False
                else:
                    new_position = (new_position[0] + speed, new_position[1])
                    check_first = True
            else:
                # All parts of veh have been in intersection
                # Calculate rotation angle
                if ((new_position[1] - 270 + speed) / (318 - 270)) * 90 > 15:
                    self.r[veh_num] = ((new_position[1] - 270 + speed) / (318 - 270)) * 90
                else:
                    self.r[veh_num] = 0

                if ((new_position[1] - 270 + speed) / (318 - 270)) * 90 > 90:
                    self.r[veh_num] = 90

                # Calculate trajectory by using Bezier Curve
                x = pow(1 - (self.beze_t[veh_num] / (318 - 270)), 2) * 270 + 2 * (self.beze_t[veh_num] / (318 - 270)) * (
                    1 - self.beze_t[veh_num] / (318 - 270)) * 318 + pow(
                    self.beze_t[veh_num] / (318 - 270), 2) * 318
                y = pow(1 - (self.beze_t[veh_num] / (318 - 270)), 2) * 283 + 2 * (self.beze_t[veh_num] / (318 - 270)) * (
                    1 - self.beze_t[veh_num] / (318 - 270)) * 283 + pow(
                    self.beze_t[veh_num] / (318 - 270), 2) * 320

                self.beze_t[veh_num] += 2
                new_position = (x, y)
                print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                print(new_position)

                # Calculate the big Square's coordinate
                self.up_left_x[veh_num] = rec_funcs.W2S_up_left_x(new_position[0], self.r[veh_num])
                self.up_left_y[veh_num] = rec_funcs.W2S_up_left_y(new_position[1])
                self.down_left_x[veh_num] = rec_funcs.W2S_down_left_x(new_position[0], self.r[veh_num])
                self.down_left_y[veh_num] = rec_funcs.W2S_down_left_y(new_position[1], self.r[veh_num])
                self.up_right_x[veh_num] = rec_funcs.W2S_up_right_x(new_position[0], self.r[veh_num])
                self.up_right_y[veh_num] = rec_funcs.W2S_up_right_y(new_position[1])
                self.down_right_x[veh_num] = rec_funcs.W2S_down_right_x(new_position[0], self.r[veh_num])
                self.down_right_y[veh_num] = rec_funcs.W2S_down_right_y(new_position[1], self.r[veh_num])

                # Up left
                if not self.collision(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num], time):
                    print("upleft, pattern1")
                    return False

                # Up right
                if not self.collision(veh_num, self.up_right_x[veh_num], self.up_right_y[veh_num], time):
                    print("upright, pattern1")
                    return False

                # Down left
                if not self.collision(veh_num, self.down_left_x[veh_num], self.down_left_y[veh_num], time):
                    print("downleft, pattern1")
                    return False

                # Down right
                if ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10) in \
                        self.intersec_grid[time]:
                    if self.intersec_grid[time][
                        ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] == False:
                            print("downright, pattern1")
                            self.beze_t[veh_num] = 2
                            return False
                    else:
                        self.intersec_grid[time][
                            (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                        self.intersec_grid[time][
                            ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                        self.intersec_grid[time][
                            (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                        self.intersec_grid[time][
                            ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] = False
                # Situation that down_right is out of the region of inter_sec grid
                else:
                    if (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10) in self.intersec_grid[
                        time]:
                        self.intersec_grid[time][
                            (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                    if ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10) in \
                            self.intersec_grid[time]:
                        self.intersec_grid[time][
                            ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                    if (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10) in \
                            self.intersec_grid[time]:
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
                                ((self.up_left_x[veh_num] + 10) // 10 * 10,
                                 self.down_left_y[veh_num] // 10 * 10)] = False
                    # y coordinate is the reason
                    if abs(self.up_left_y[veh_num] - self.down_left_y[veh_num]) > 10:
                        if (self.up_left_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10) in \
                                self.intersec_grid[time]:
                            self.intersec_grid[time][
                                (self.up_left_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10)] = False
                        if (self.up_right_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10) in \
                                self.intersec_grid[time]:
                            self.intersec_grid[time][
                                (
                                self.up_right_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10)] = False

            if check_first:
                self.intersec_grid[time][(270, 270)] = False
            check_first = False

            # print("check p1 current_time", current_time)
            # print('time', time)
            # print(self.beze_t[veh_num])
            # print('new_position', new_position, 'r', self.r)
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
    def light_veh_pattern2(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0

        # to light up grid(320, 300)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern2')

        # Before veh get out of the intersection
        while new_position[1] < destination[1]:

            # Calculate trajectory by using Bezier Curve
            x = new_position[0]
            y = new_position[1] + speed

            new_position = (x, y)

            # Calculate the big Square's coordinate
            self.up_left_x[veh_num] = new_position[0]
            self.up_left_y[veh_num] = new_position[1]
            self.down_left_x[veh_num] = new_position[0]
            self.down_left_y[veh_num] = new_position[1] + 10
            self.up_right_x[veh_num] = new_position[0] + 5
            self.up_right_y[veh_num] = new_position[1]
            self.down_right_x[veh_num] = new_position[0] + 5
            self.down_right_y[veh_num] = new_position[1] + 10

            # Up left
            if not self.collision(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num], time):
                print("upleft, pattern2")
                return False

            # Up right
            if not self.collision(veh_num, self.up_right_x[veh_num], self.up_right_y[veh_num], time):
                print("upright, pattern2")
                return False

            # Down left
            if not self.collision(veh_num, self.down_left_x[veh_num], self.down_left_y[veh_num], time):
                print("downleft, pattern2")
                return False

            # Down right
            if ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10) in \
                    self.intersec_grid[time]:
                if self.intersec_grid[time][(self.down_right_x[veh_num] // 10 * 10,
                                             self.down_right_y[veh_num] // 10 * 10)] == False:
                        print("downright, pattern2")
                        self.beze_t[veh_num] = 2
                        return False
                else:
                    self.intersec_grid[time][
                        (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                    self.intersec_grid[time][
                        ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                    self.intersec_grid[time][
                        (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                    self.intersec_grid[time][(
                        (self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] = False

            else:
                if (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10) in self.intersec_grid[
                    time]:
                    self.intersec_grid[time][
                        (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                if ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10) in \
                        self.intersec_grid[time]:
                    self.intersec_grid[time][
                        ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                if (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10) in \
                        self.intersec_grid[time]:
                    self.intersec_grid[time][
                        (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False


            # print("check p2 current_time", current_time)
            # print(self.intersec_grid[time])
            # print('time', time)
            # print('veh_num', veh_num)
            # print(self.beze_t)
            # print(self.beze_t[veh_num])
            # print('new_position', new_position, 'r', self.r)
            # print(self.intersec_grid[time])
            time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

    # vehicles travel from E_5 to W_5
    # origin and destination is a pattern of (x,y)
    def light_veh_pattern3(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern3')

        # Before veh get out of the intersection
        while new_position[0] > destination[0] - 10:

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
            if not self.collision(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num], time):
                print("upleft, pattern3")
                return False

            # Up right
            if not self.collision(veh_num, self.up_right_x[veh_num], self.up_right_y[veh_num], time):
                print("upright, pattern3")
                return False

            # Down left
            if not self.collision(veh_num, self.down_left_x[veh_num], self.down_left_y[veh_num], time):
                print("downleft, pattern3")
                return False

            # Down right
            if ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10) in \
                    self.intersec_grid[time]:
                if self.intersec_grid[time][(self.down_right_x[veh_num] // 10 * 10,
                                             self.down_right_y[veh_num] // 10 * 10)] == False:
                        print("downright, pattern3")
                        return False
                else:
                    self.intersec_grid[time][
                        (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                    self.intersec_grid[time][
                        ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                    self.intersec_grid[time][
                        (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                    self.intersec_grid[time][
                        ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] = False

            else:
                if (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10) in self.intersec_grid[time]:
                    self.intersec_grid[time][
                        (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                if ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10) in self.intersec_grid[
                    time]:
                    self.intersec_grid[time][
                        ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                if (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10) in self.intersec_grid[
                    time]:
                    self.intersec_grid[time][
                        (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False

            # print("check p3 current_time", current_time)
            # print(self.intersec_grid[time])
            # print('time', time)
            # print(self.beze_t[veh_num])
            # print(self.up_left_x[veh_num], self.up_left_y[veh_num])
            # print(self.up_right_x[veh_num], self.up_right_y[veh_num])
            # print(self.down_left_x[veh_num], self.down_left_y[veh_num])
            # print(self.down_right_x[veh_num], self.down_right_y[veh_num])
            # print('new_position', new_position, 'r', self.r)
            # print(self.intersec_grid[time])
            time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

    # vehicles travel from S_3 to W_4
    # origin and destination is a pattern of (x,y)
    def light_veh_pattern4(self, veh_num, current, origin, destination, speed, current_time):

        new_position = current
        time = 0

        # To light up grid(270, 270)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern4')

        # Before veh get out of the intersection
        while new_position[0] > destination[0]:
            print('***************************************************')
            # Check if all parts of veh have been in intersection
            if origin[1] - (new_position[1] - speed) <= 10:
                if not self.intersec_grid[time][(290, 320)]:
                    print('firstgrid')
                    return False
                else:
                    new_position = (new_position[0], new_position[1] - speed)
                    check_first = True
            else:
                # All parts of veh have been in intersection
                # Calculate rotation angle
                if ((330 - new_position[1] - speed) / 22) * 90 > 15:
                    self.r[veh_num] = ((330 - new_position[1] - speed) / 22) * 90
                else:
                    self.r[veh_num] = 0

                if ((330 - new_position[1] - speed) / 22) * 90 > 90:
                    self.r[veh_num] = 90

                # Calculate trajectory by using Bezier Curve
                x = pow(1 - (self.beze_t[veh_num] / 22), 2) * 293 + 2 * (self.beze_t[veh_num] / 22) * (
                    1 - self.beze_t[veh_num] / 22) * 293 + pow(
                    self.beze_t[veh_num] / 22, 2) * 270
                y = pow(1 - (self.beze_t[veh_num] / 22), 2) * 320 + 2 * (self.beze_t[veh_num] / 22) * (
                    1 - self.beze_t[veh_num] / 22) * 306 + pow(
                    self.beze_t[veh_num] / 22, 2) * 306

                self.beze_t[veh_num] += 2
                new_position = (x, y)
                print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                print(new_position)

                # Calculate the big Square's coordinate
                self.up_left_x[veh_num] = rec_funcs.S2W_up_left_x(new_position[0])
                self.up_left_y[veh_num] = rec_funcs.S2W_up_left_y(new_position[1], self.r[veh_num])
                self.down_left_x[veh_num] = rec_funcs.S2W_down_left_x(new_position[0])
                self.down_left_y[veh_num] = rec_funcs.S2W_down_left_y(new_position[1], self.r[veh_num])
                self.up_right_x[veh_num] = rec_funcs.S2W_up_right_x(new_position[0], self.r[veh_num])
                self.up_right_y[veh_num] = rec_funcs.S2W_up_right_y(new_position[1], self.r[veh_num])
                self.down_right_x[veh_num] = rec_funcs.S2W_down_right_x(new_position[0], self.r[veh_num])
                self.down_right_y[veh_num] = rec_funcs.S2W_down_right_y(new_position[1], self.r[veh_num])

                # Up left
                if not self.collision(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num], time):
                    print("upleft, pattern4")
                    return False

                # Up right
                if not self.collision(veh_num, self.up_right_x[veh_num], self.up_right_y[veh_num], time):
                    print("upright, pattern4")
                    return False

                # Down left
                if not self.collision(veh_num, self.down_left_x[veh_num], self.down_left_y[veh_num], time):
                    print("downleft, pattern4")
                    return False

                # Down right
                if ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10) in \
                        self.intersec_grid[time]:
                    if self.intersec_grid[time][
                        ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] == False:
                            print('downright')
                            self.beze_t[veh_num] = 2
                            return False
                    else:
                        self.intersec_grid[time][
                            (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                        self.intersec_grid[time][
                            ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                        self.intersec_grid[time][
                            (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                        self.intersec_grid[time][
                            ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] = False
                # Situation that down_right is out of the region of inter_sec grid
                else:
                    if (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10) in self.intersec_grid[
                        time]:
                        self.intersec_grid[time][
                            (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                    if ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10) in \
                            self.intersec_grid[time]:
                        self.intersec_grid[time][
                            ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                    if (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10) in \
                            self.intersec_grid[time]:
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
                                ((self.up_left_x[veh_num] + 10) // 10 * 10,
                                 self.down_left_y[veh_num] // 10 * 10)] = False
                    # y coordinate is the reason
                    if abs(self.up_left_y[veh_num] - self.down_left_y[veh_num]) > 10:
                        if (self.up_left_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10) in \
                                self.intersec_grid[time]:
                            self.intersec_grid[time][
                                (self.up_left_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10)] = False
                        if (self.up_right_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10) in \
                                self.intersec_grid[time]:
                            self.intersec_grid[time][
                                (
                                self.up_right_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10)] = False

            if check_first:
                self.intersec_grid[time][(290, 320)] = False
            check_first = False

            # print("check p4 current_time", current_time)
            # print('time', time)
            # print(self.beze_t[veh_num])
            # print('new_position', new_position, 'r', self.r)
            # print(self.intersec_grid[time])
            time += 1

        # Initiate beze_t
        self.beze_t[veh_num] = 2

        return True

    # origin and destination is a pattern of (x,y)
    def light_veh_pattern5(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0

        # To light up grid(270, 270)
        check_first = False

        # Initiate intersection grid
        if self.time_step == 0:
            self.init_intersec_grid(self.t_ahead)

        if current_time > self.time_step:
            self.update_intersec_grid(current_time, self.time_step, veh_num)
            print('Pattern5')

        # Before veh get out of the intersection
        while new_position[0] < destination[0]:

            # Check if all parts of veh have been in intersection
            if new_position[1] - speed >= origin[0] + 2:
                if not self.intersec_grid[time][(270, 270)]:
                    print('firstgrid')
                    return False
                else:
                    new_position = (new_position[0] + speed, new_position[1])
                    check_first = True
            else:
                # All parts of veh have been in intersection
                # Calculate rotation angle
                if ((new_position[1] - 270 + speed) / 60) * 90 > 15:
                    self.r[veh_num] = ((new_position[1] - 270 + 3) / 60) * 90
                else:
                    self.r[veh_num] = 0

                if ((new_position[1] - 270 + speed) / 60) * 90 > 90:
                    self.r[veh_num] = 90

                # Calculate trajectory by using Bezier Curve
                x = pow(1 - (self.beze_t[veh_num] / 60), 2) * 270 + 2 * (self.beze_t[veh_num] / 60) * (
                    1 - self.beze_t[veh_num] / 60) * 330 + pow(
                    self.beze_t[veh_num] / 60, 2) * 330
                y = pow(1 - (self.beze_t[veh_num] / 60), 2) * 273 + 2 * (self.beze_t[veh_num] / 60) * (
                    1 - self.beze_t[veh_num] / 60) * 273 + pow(
                    self.beze_t[veh_num] / 60, 2) * 330

                self.beze_t[veh_num] += 2
                # if x >= 328:
                #     new_position = (x, y + speed)
                new_position = (x, y)
                # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                # print(new_position)

                # Calculate the big Square's coordinate
                self.up_left_x[veh_num] = rec_funcs.W2S_up_left_x(new_position[0], self.r[veh_num])
                self.up_left_y[veh_num] = rec_funcs.W2S_up_left_y(new_position[1])
                self.down_left_x[veh_num] = rec_funcs.W2S_down_left_x(new_position[0], self.r[veh_num])
                self.down_left_y[veh_num] = rec_funcs.W2S_down_left_y(new_position[1], self.r[veh_num])
                self.up_right_x[veh_num] = rec_funcs.W2S_up_right_x(new_position[0], self.r[veh_num])
                self.up_right_y[veh_num] = rec_funcs.W2S_up_right_y(new_position[1])
                self.down_right_x[veh_num] = rec_funcs.W2S_down_right_x(new_position[0], self.r[veh_num])
                self.down_right_y[veh_num] = rec_funcs.W2S_down_right_y(new_position[1], self.r[veh_num])

                # Up left
                if not self.collision(veh_num, self.up_left_x[veh_num], self.up_left_y[veh_num], time):
                    print("upleft, pattern1")
                    return False

                # Up right
                if not self.collision(veh_num, self.up_right_x[veh_num], self.up_right_y[veh_num], time):
                    print("upright, pattern1")
                    return False

                # Down left
                if not self.collision(veh_num, self.down_left_x[veh_num], self.down_left_y[veh_num], time):
                    print("downleft, pattern1")
                    return False

                # Down right
                if ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10) in \
                        self.intersec_grid[time]:
                    if self.intersec_grid[time][
                        ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] == False:
                            print("downright, pattern1")
                            self.beze_t[veh_num] = 2
                            return False
                    else:
                        self.intersec_grid[time][
                            (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                        self.intersec_grid[time][
                            ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                        self.intersec_grid[time][
                            (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                        self.intersec_grid[time][
                            ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] = False
                # Situation that down_right is out of the region of inter_sec grid
                else:
                    if (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10) in self.intersec_grid[
                        time]:
                        self.intersec_grid[time][
                            (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                    if ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10) in \
                            self.intersec_grid[time]:
                        self.intersec_grid[time][
                            ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                    if (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10) in \
                            self.intersec_grid[time]:
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
                                ((self.up_left_x[veh_num] + 10) // 10 * 10,
                                 self.down_left_y[veh_num] // 10 * 10)] = False
                    # y coordinate is the reason
                    if abs(self.up_left_y[veh_num] - self.down_left_y[veh_num]) > 10:
                        if (self.up_left_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10) in \
                                self.intersec_grid[time]:
                            self.intersec_grid[time][
                                (self.up_left_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10)] = False
                        if (self.up_right_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10) in \
                                self.intersec_grid[time]:
                            self.intersec_grid[time][
                                (
                                self.up_right_x[veh_num] // 10 * 10, (self.up_left_y[veh_num] + 10) // 10 * 10)] = False

            if check_first:
                self.intersec_grid[time][(270, 270)] = False
            check_first = False

            # print("check p1 current_time", current_time)
            # print('time', time)
            # print(self.beze_t[veh_num])
            # print('new_position', new_position, 'r', self.r)
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