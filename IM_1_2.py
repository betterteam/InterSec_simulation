# coding:utf-8
# Test Intersection Manager with UDP
# Get vehicle proposal, return the result
# Starting of installing the collision detect algorithm
# Unify into a class
# Add light_veh_pattern3

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
        self.t_ahead = 36

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
            self.beze_t.append(0)
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

            #print(recData)
            #print(recData["arrival_time"])

            veh_id = recData["Veh_id"]
            current = tuple(recData["position"])
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
                    print("self.sendData", self.sendData)
                    print("recData:", recData)
                    self.sendData[recData["Veh_id"]]["result"] = 1
                else:
                    #print("self.sendData", self.sendData)
                    #print("recData:", recData)
                    self.sendData[recData["Veh_id"]]["result"] = 0

            # if recData["arrival_time"] < 5:
            #     self.sendData[recData["Veh_id"]]["result"] = 1

            #print(self.sendData)

            # Send Json
            mes = bytes(json.dumps(self.sendData[recData["Veh_id"]]), encoding='utf-8')
            self.server.sendto(mes, client)

        self.server.close()

    # vehicles travel from W_1 to S_6
    # origin and destination is a pattern of (x,y)
    def light_veh_pattern1(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0
        check_grid = []
        return_time = 0
        #print("check p1 current_time", current_time)

        # Initiate intersection grid
        if current_time > self.time_step:
            self.time_step = current_time
            #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            for k in range(self.t_ahead):
                for i in range(270, 330, 10):
                    for j in range(270, 330, 10):
                        self.intersec_grid[k][(i, j)] = True

            # for i in range(self.t_ahead - 1):
            #     self.intersec_grid[i] = self.intersec_grid[i+1]
            #
            # for i in range(270, 330, 10):
            #     for j in range(270, 330, 10):
            #         self.intersec_grid[self.t_ahead][(i, j)] = True

        # Before veh get out of the intersection
        while new_position[1] <= destination[1]:

            # Check if all parts of veh have been in intersection
            if new_position[0] + speed < origin[0]:
                if not self.intersec_grid[time][(270, 270)]:
                    return False
                    #break
                else:
                    new_position = (new_position[0] + speed, new_position[1])
                    self.intersec_grid[time][(270, 270)] = False
            else:
                # Calculate rotation angle
                if (((new_position[1] - 270 + speed) / 60) * 90 > 15):
                    self.r[veh_num] = ((new_position[1] - 270 + 3) / 60) * 90
                else:
                    self.r[veh_num] = 0

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
                print(time)
                if (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10) in self.intersec_grid[time]:
                    if self.intersec_grid[time][(self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] == False:
                        return False
                    else:
                        self.intersec_grid[time][(self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                        check_grid.append((self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10))
                        # print(time)
                        # print(new_position)
                        # print((self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10))
                        # print('success')

                # Up right
                if ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10) in self.intersec_grid[time]:
                    if self.intersec_grid[time][((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] == False:
                        if ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10) not in check_grid:
                            return False
                        else:
                            self.intersec_grid[time][((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                            check_grid.append(((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10))
                    else:
                        self.intersec_grid[time][((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                        check_grid.append(((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10))
                        # print(time)
                        # print(new_position)
                        # print((self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10))
                        # print('success')

                # Down left
                if (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10) in self.intersec_grid[time]:
                    if self.intersec_grid[time][(self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] == False:
                        if (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10) not in check_grid:
                            return False
                        else:
                            self.intersec_grid[time][(self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                            check_grid.append((self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10))
                    else:
                        self.intersec_grid[time][(self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                        check_grid.append((self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10))
                        # print(time)
                        # print(new_position)
                        # print((self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10))
                        # print('success')

                # Down right
                if ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10) in self.intersec_grid[time]:
                    if self.intersec_grid[time][((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] == False:
                        if ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10) not in check_grid:
                            return False
                        else:
                            self.intersec_grid[time][((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] = False
                    else:
                        self.intersec_grid[time][((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] = False
                        # print(time)
                        # print(new_position)
                        # print((self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10))
                        # print('success')

            print("check p1 current_time", current_time)
            print(self.intersec_grid[time])
            check_grid = []
            time += 1

            # if time > 8:
            #     break


        #print(time)
        if time == 35:
            for i in range(self.t_ahead):
                print(self.intersec_grid[i])

        return True

    # vehicles travel from E_5 to W_5
    # origin and destination is a pattern of (x,y)
    def light_veh_pattern3(self, veh_num, current, origin, destination, speed, current_time):
        new_position = current
        time = 0
        check_grid = []
        return_time = 0
        print("check p3 current_time", current_time)
        print(self.intersec_grid)

        # Initiate intersection grid
        if current_time > self.time_step:
            self.time_step = current_time
            #print("+++++++++++++++++++++++++++++++")
            for k in range(self.t_ahead):
                for i in range(270, 330, 10):
                    for j in range(270, 330, 10):
                        self.intersec_grid[k][(i, j)] = True

            # for i in range(self.t_ahead - 1):
            #     self.intersec_grid[i] = self.intersec_grid[i+1]
            #
            # for i in range(270, 330, 10):
            #     for j in range(270, 330, 10):
            #         self.intersec_grid[self.t_ahead][(i, j)] = True

        # Before veh get out of the intersection
        while new_position[0] >= destination[0]:

            # Check if all parts of veh have been in intersection
            if new_position[0] - speed < origin[0]:
                #print("current_time", current_time)
                #print("timestep", self.time_step)
                #print("time", time)
                #print("intersec_grid", self.intersec_grid)
                if not self.intersec_grid[time][(320, 300)]:
                    print("check", 1)
                    return False
                else:
                    new_position = (new_position[0] - speed, new_position[1])
                    self.intersec_grid[time][(320, 300)] = False
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
                        print("check", 2)
                        return False
                    else:
                        self.intersec_grid[time][
                            (self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10)] = False
                        check_grid.append((self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10))
                        # print(time)
                        # print(new_position)
                        # print((self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10))
                        # print('success')

                # Up right
                if ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10) in \
                        self.intersec_grid[time]:
                    if self.intersec_grid[time][
                        ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] == False:
                        if ((self.up_right_x[veh_num]) // 10 * 10,
                            self.up_right_y[veh_num] // 10 * 10) not in check_grid:
                            print("check", 3)
                            return False
                        else:
                            self.intersec_grid[time][(
                            (self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                            check_grid.append(
                                ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10))
                    else:
                        self.intersec_grid[time][
                            ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10)] = False
                        check_grid.append(
                            ((self.up_right_x[veh_num]) // 10 * 10, self.up_right_y[veh_num] // 10 * 10))
                        # print(time)
                        # print(new_position)
                        # print((self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10))
                        # print('success')

                # Down left
                if (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10) in \
                        self.intersec_grid[time]:
                    if self.intersec_grid[time][
                        (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] == False:
                        if (self.down_left_x[veh_num] // 10 * 10,
                            (self.down_left_y[veh_num]) // 10 * 10) not in check_grid:
                            print("check", 4)
                            return False
                        else:
                            self.intersec_grid[time][(
                            self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                            check_grid.append(
                                (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10))
                    else:
                        self.intersec_grid[time][
                            (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10)] = False
                        check_grid.append(
                            (self.down_left_x[veh_num] // 10 * 10, (self.down_left_y[veh_num]) // 10 * 10))
                        # print(time)
                        # print(new_position)
                        # print((self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10))
                        # print('success')

                # Down right
                if ((self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10) in \
                        self.intersec_grid[time]:
                    if self.intersec_grid[time][((self.down_right_x[veh_num]) // 10 * 10,
                                                 (self.down_right_y[veh_num]) // 10 * 10)] == False:
                        if ((self.down_right_x[veh_num]) // 10 * 10,
                            (self.down_right_y[veh_num]) // 10 * 10) not in check_grid:
                            print("check", 5)
                            return False
                        else:
                            self.intersec_grid[time][((self.down_right_x[veh_num]) // 10 * 10,
                                                      (self.down_right_y[veh_num]) // 10 * 10)] = False
                    else:
                        self.intersec_grid[time][(
                        (self.down_right_x[veh_num]) // 10 * 10, (self.down_right_y[veh_num]) // 10 * 10)] = False
                        # print(time)
                        # print(new_position)
                        # print((self.up_left_x[veh_num] // 10 * 10, self.up_left_y[veh_num] // 10 * 10))
                        # print('success')

            check_grid = []
            time += 1

        for i in range(time):
            print(self.intersec_grid[time])
        #print(time)
        if time == 35:
            for i in range(self.t_ahead):
                print(self.intersec_grid[i])

        return True






# def test_collision():
#     print()

#print(light_veh_pattern1(1, (262, 273), (270, 273), (330, 330), 2, 0))

if __name__ == '__main__':
    test = IM().sendResult()
    #IM.sendResult()
    #sys.exit(test.exec_())