# coding:utf-8
# From 180102
# With two traffic lines

import sys
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFrame, QDesktopWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QTimer, QTime
import math

import socket
from datetime import datetime
import struct
import json
from enum import Enum, unique

sys.path.append('Users/better/PycharmProjects/GUI_Qt5/Intersection/Intersection_Ex')
import draw_intersec
import draw_veh

class Position:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

@unique
class Direction(Enum):
    Left = 1
    Right = 2
    Up = 3
    Down = 4

class Speed:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Size:
    def __init__(self, x=5, y=10):
        self.x = x
        self.y = y

class Vehicle:
    # def __init__(self, direction):
    #     self._position = Position()
    #     self._speed = Speed()
    #     self._size = Size()
        # self._direction = direction

    def __init__(self):
        self._position = Position()
        self._speed = Speed()
        self._size = Size()

    def setPosition(self, position):
        self._position = position

    def getPosition(self):
        return self._position

    def setDirection(self, direction):
        self._direction = direction

    def getDirection(self):
        return self._direction

    def setSpeed(self, speed):
        self._speed = speed

    def getSpeed(self):
        return self._speed

    def setSize(self, size):
        self._size = size

    def getSize(self):
        return self._size

    # 根据self中direcion知道现在点，根据direction（数组中参数，即目的地），从而得知在十字路口中的行进方式（路径）
    def proceed_style(self, direction):
        if direction == 1:
            return 1


class Example(QWidget):
    def __init__(self, sendData_1, sendData_2, sendData_3, sendData_4, sendData_5, sendData_Ex1):
        super().__init__()
        self.sendData_1 = sendData_1
        self.sendData_2 = sendData_2
        self.sendData_3 = sendData_3
        self.sendData_4 = sendData_4
        self.sendData_5 = sendData_5
        self.sendData_Ex1 = sendData_Ex1
        self.my_result = 0
        self.t_t = 0

        self.ti = 0
        self.beze_t = []
        self.r = []
        self.intersec1_vehnum = 0
        self.intersec4_vehnum = 0
        self.veh_flag = []

        self.N5_1E2_beze_t = []
        self.N5_1E2_r = []

        self.S2_1W5_beze_t = []
        self.S2_1W5_r = []

        self.W2_1N2_beze_t = []
        self.W2_1N2_r = []

        self.E5_1S5_beze_t = []
        self.E5_1S5_r = []

        self.N5_1W5_beze_t = []
        self.N5_1W5_r = []

        self.S2_1E2_beze_t = []
        self.S2_1E2_r = []

        self.W2_1S5_beze_t = []
        self.W2_1S5_r = []

        self.E5_1N2_beze_t = []
        self.E5_1N2_r = []

        self.Ex1_beze_t = []
        self.Ex1_r = []

        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000/60)#一秒間隔で更新

        self.t = QTime()
        self.t.start()
        self.show()

    def initUI(self):
        self.setGeometry(0, 0, 930, 930)
        self.setWindowTitle("Koku's Simulation")

        for i in range(10):
            self.beze_t.append(2)
            self.r.append(0)

            self.N5_1E2_beze_t.append(2)
            self.N5_1E2_r.append(0)

            self.S2_1W5_beze_t.append(2)
            self.S2_1W5_r.append(0)

            self.W2_1N2_beze_t.append(2)
            self.W2_1N2_r.append(0)

            self.E5_1S5_beze_t.append(2)
            self.E5_1S5_r.append(0)

            self.N5_1W5_beze_t.append(2)
            self.N5_1W5_r.append(0)

            self.S2_1E2_beze_t.append(2)
            self.S2_1E2_r.append(0)

            self.W2_1S5_beze_t.append(2)
            self.W2_1S5_r.append(0)

            self.W2_1S5_beze_t.append(2)
            self.W2_1S5_r.append(0)

            self.E5_1N2_beze_t.append(2)
            self.E5_1N2_r.append(0)

            self.Ex1_beze_t.append(2)
            self.Ex1_r.append(0)

        for i in range(60):
            self.veh_flag.append(False)


        self.single_0_0 = True
        self.single_0_1 = True

        self.collision_check = []
        self.collision_check_N = []
        self.collision_check_S = []
        self.collision_check_W = []
        self.collision_check_E = []
        self.collision_check_N2 = []
        self.collision_check_Ex1 = []

        self.grid = {}

        for i in range(270, 330, 10):
            for j in range(270, 330, 10):
                self.grid[(i, j)] = True

    def paintEvent(self, e):
        self.t_t += 1
        qp = QPainter(self)

        draw_intersec.drawLines(qp)
        #self.drawSignals_0(qp)
        self.drawVehicles(qp)

    def propose(self, current, current_time, sendData, address):
        server_address = ('localhost', 6789 + address)
        max_size = 4096

        # print('Starting the client at', datetime.now())

        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        current_position = list(current)

        # sendData_1: veh info and current Total_time
        dictMerge = dict({"time_step": current_time}, **sendData)
        dictMerge = dict({"current_position": current_position}, **dictMerge)
        mes = bytes(json.dumps(dictMerge), encoding='utf-8')

        client.sendto(mes, server_address)
        data, server = client.recvfrom(max_size)

        data = data.decode('utf-8')
        recData = json.loads(data)
        # print('At', datetime.now(), server, 'said', recData)
        client.close()
        self.my_result = recData['result']

        return self.my_result

    def calculate_vehnum(self, i, old_x, old_y, new_x, new_y, sendData):
        old_flag = self.veh_flag[sendData["vehicle"][i]["Veh_id"]]
        if 270 <= new_x <= 330 and 270 <= new_y <= 330:
            self.veh_flag[sendData["vehicle"][i]["Veh_id"]] = True
            new_flag = True
            if not old_flag and new_flag:
                self.intersec1_vehnum += 1
        elif 0 <= old_x < 270 and 0 <= new_x < 270 and new_x >= old_x:
            self.veh_flag[sendData["vehicle"][i]["Veh_id"]] = True
            new_flag = True
            if not old_flag and new_flag:
                self.intersec1_vehnum += 1
        elif 330 < old_x < 600 and 330 < new_x < 600 and new_x <= old_x:
            self.veh_flag[sendData["vehicle"][i]["Veh_id"]] = True
            new_flag = True
            if not old_flag and new_flag:
                self.intersec1_vehnum += 1
        elif 0 <= old_y < 270 and 0 <= new_y < 270 and new_y >= old_y:
            self.veh_flag[sendData["vehicle"][i]["Veh_id"]] = True
            new_flag = True
            if not old_flag and new_flag:
                self.intersec1_vehnum += 1
        elif 330 < old_y < 600 and 330 < new_y < 600 and new_y <= old_y:
            self.veh_flag[sendData["vehicle"][i]["Veh_id"]] = True
            new_flag = True
            if not old_flag and new_flag:
                self.intersec1_vehnum += 1
        else:
            self.veh_flag[sendData["vehicle"][i]["Veh_id"]] = False
            new_flag = False
            if old_flag and not new_flag:
                self.intersec1_vehnum -= 1

    def calculate_vehnum_inside(self, i, sendData):
        old_flag = self.veh_flag[sendData["vehicle"][i]["Veh_id"]]
        self.veh_flag[sendData["vehicle"][i]["Veh_id"]] = True
        new_flag = True
        if not old_flag and new_flag:
            self.intersec1_vehnum += 1

    def calculate_vehnum_4(self, i, old_x, old_y, new_x, new_y, sendData):
        old_flag = self.veh_flag[sendData["vehicle"][i]["Veh_id"]]
        if 600 <= new_x <= 660 and 600 <= new_y <= 660:
            self.veh_flag[sendData["vehicle"][i]["Veh_id"]] = True
            new_flag = True
            if not old_flag and new_flag:
                self.intersec4_vehnum += 1
        elif 330 <= old_x < 600 and 330 <= new_x < 600 and new_x >= old_x:
            self.veh_flag[sendData["vehicle"][i]["Veh_id"]] = True
            new_flag = True
            if not old_flag and new_flag:
                self.intersec4_vehnum += 1
        elif 660 < old_x < 930 and 660 < new_x < 930 and new_x <= old_x:
            self.veh_flag[sendData["vehicle"][i]["Veh_id"]] = True
            new_flag = True
            if not old_flag and new_flag:
                self.intersec4_vehnum += 1
        elif 330 <= old_y < 600 and 330 <= new_y < 600 and new_y >= old_y:
            self.veh_flag[sendData["vehicle"][i]["Veh_id"]] = True
            new_flag = True
            if not old_flag and new_flag:
                self.intersec4_vehnum += 1
        elif 660 < old_y < 930 and 660 < new_y < 930 and new_y <= old_y:
            self.veh_flag[sendData["vehicle"][i]["Veh_id"]] = True
            new_flag = True
            if not old_flag and new_flag:
                self.intersec4_vehnum += 1
        else:
            self.veh_flag[sendData["vehicle"][i]["Veh_id"]] = False
            new_flag = False
            if old_flag and not new_flag:
                self.intersec4_vehnum -= 1

    def calculate_vehnum_4_inside(self, i, sendData):
        old_flag = self.veh_flag[sendData["vehicle"][i]["Veh_id"]]
        self.veh_flag[sendData["vehicle"][i]["Veh_id"]] = True
        new_flag = True
        if not old_flag and new_flag:
            self.intersec4_vehnum += 1

    # a vertical vehicle marks his own place
    def mark_own_v(self, collision_check, x, y):
        for i in range(-10, 11):
            collision_check.append((x, y + i))

    # a tropical vehicle marks his own place
    def mark_own_t(self, collision_check, x, y):
        for i in range(-10, 11):
            collision_check.append((x + i, y))

    # a vertical vehicle delete his own marked place
    def delete_own_v(self, collision_check, x, y):
        for i in range(-10, 11):
            collision_check.remove((x, y + i))

    # a tropical vehicle delete his own marked place
    def delete_own_t(self, collision_check, x, y):
        for i in range(-10, 11):
            collision_check.remove((x + i, y))

    def drawVehicles(self, qp):

        qp.setPen(Qt.black)
        qp.setBrush(Qt.green)

        # Vehicles Pattern2(from 1N5 to 1S5)
        for i, veh in enumerate(vehicles_1N5_1S5):
            # Make sure if there is a vehicle ahead
            if (veh.getPosition().x + veh.getSpeed().x, veh.getPosition().y + veh.getSpeed().y) in self.collision_check_N:
                # Influential veh_num calculation
                self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y, veh.getPosition().x, veh.getPosition().y, self.sendData_2)
                draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                # Declare the region where myself(vehicle) will be
                self.mark_own_v(self.collision_check_N, veh.getPosition().x, veh.getPosition().y)
                # for j in range(-10, 11):
                #     self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y + j))
            else:
                # In the next timestep, will be possible to enter intersection_1
                if veh.getPosition().y + veh.getSpeed().y > 265 and veh.getPosition().y <= 264:
                    # Try to make a reservation from IM.
                    # If TRUE, then enter the intersection in next timestep.
                    # if self.propose((veh.getPosition().x, veh.getPosition().y), self.t_t, self.sendData_2["vehicle"][i], 0):
                    if False:
                        print(self.t_t, 'True')
                        # for j in range(-10, 11):
                        #     self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y + j))
                        veh.getPosition().y += veh.getSpeed().y
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y, self.sendData_2)
                        # If vehicle reaches the goal, start from the beginning
                        if veh.getPosition().y > 600:
                            veh.getPosition().y = 0
                        # sketch new position
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        # Declare the region where myself(vehicle) will be
                        self.mark_own_v(self.collision_check_N, veh.getPosition().x, veh.getPosition().y)
                        # for j in range(-10, 11):
                        #     self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y + j))
                    # If FALSE, then stop before entering into intersection.
                    else:
                        print(self.t_t, 'False')
                        self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_2)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        self.mark_own_v(self.collision_check_N, veh.getPosition().x, veh.getPosition().y)
                        # for j in range(-10, 11):
                        #     self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y + j))
                # Just proceed
                else:
                    veh.getPosition().y += veh.getSpeed().y
                    # Influential veh_num calculation
                    old_x = veh.getPosition().x - veh.getSpeed().x
                    old_y = veh.getPosition().y - veh.getSpeed().y
                    self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y, self.sendData_2)
                    # If vehicle reaches the goal, start from the beginning
                    if veh.getPosition().y > 600:
                        veh.getPosition().y = 0
                    # sketch new position
                    draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                    self.mark_own_v(self.collision_check_N, veh.getPosition().x, veh.getPosition().y)
                    # for j in range(5):
                    #     self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y + j))

        # Vehicles Pattern2-2(from 1S2 to 1N2)
        for i, veh in enumerate(vehicles_1S2_1N2):
            # Make sure if there is a vehicle ahead
            if (veh.getPosition().x + veh.getSpeed().x,
                veh.getPosition().y + veh.getSpeed().y) in self.collision_check_S:
                # Influential veh_num calculation
                self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y, veh.getPosition().x,
                                      veh.getPosition().y, self.sendData_2)
                print(veh.getPosition().x, veh.getPosition().y)
                draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                # Declare the region where myself(vehicle) will be
                for j in range(-10, 11):
                    self.collision_check_S.append((veh.getPosition().x, veh.getPosition().y + j))
            else:
                # In the next timestep, will be possible to enter intersection_1
                if veh.getPosition().y + veh.getSpeed().y < 325 and veh.getPosition().y >= 326:
                    # Try to make a reservation from IM.
                    # If TRUE, then enter the intersection in next timestep.
                    if self.propose((veh.getPosition().x, veh.getPosition().y), self.t_t,
                                    self.sendData_2["vehicle"][i+3], 0):
                    # if True:
                        veh.getPosition().y += veh.getSpeed().y
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y,
                                              self.sendData_2)
                        # If vehicle reaches the goal, start from the beginning
                        if veh.getPosition().y < 0:
                            veh.getPosition().y = 600
                        # sketch new position
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        # Declare the region where myself(vehicle) will be
                        for j in range(-10, 11):
                            self.collision_check_S.append(
                                (veh.getPosition().x, veh.getPosition().y + j))
                    # If FALSE, then stop before entering into intersection.
                    else:
                        self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y,
                                              veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_2)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_S.append(
                                (veh.getPosition().x, veh.getPosition().y + j))
                # Just proceed
                else:
                    veh.getPosition().y += veh.getSpeed().y
                    # Influential veh_num calculation
                    old_x = veh.getPosition().x - veh.getSpeed().x
                    old_y = veh.getPosition().y - veh.getSpeed().y
                    self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y,
                                          self.sendData_2)
                    # If vehicle reaches the goal, start from the beginning
                    if veh.getPosition().y < 0:
                        veh.getPosition().y = 600
                    # sketch new position
                    draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                    for j in range(-10, 11):
                        self.collision_check_S.append((veh.getPosition().x, veh.getPosition().y + j))

        # Vehicle Pattern2-3(From 1W2 to 1E2)
        for i, veh in enumerate(vehicles_1W2_1E2):
            if (veh.getPosition().x + veh.getSpeed().x,
                veh.getPosition().y + veh.getSpeed().y) in self.collision_check_W:
                draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                for j in range(-10, 11):
                    self.collision_check_W.append((veh.getPosition().x + j, veh.getPosition().y))
            else:
                if 264 >= veh.getPosition().x and veh.getPosition().x + veh.getSpeed().x > 265:
                    if self.propose((veh.getPosition().x, veh.getPosition().y), self.t_t,
                                    self.sendData_2["vehicle"][i+6], 0):
                    # if True:
                        veh.getPosition().x += veh.getSpeed().x

                        if veh.getPosition().x > 600:
                            veh.getPosition().x = 0

                        qp.drawPoint(veh.getPosition().x + 1, veh.getPosition().y - 1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_W.append((veh.getPosition().x + j, veh.getPosition().y))
                    else:
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_W.append((veh.getPosition().x + j, veh.getPosition().y))

                else:
                    veh.getPosition().x += veh.getSpeed().x

                    if veh.getPosition().x > 600:
                        veh.getPosition().x = 0

                    draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                    for j in range(-10, 11):
                        self.collision_check_W.append((veh.getPosition().x + j, veh.getPosition().y))

        # Vehicle Pattern2-4(From 1E5 to 1W5)
        for i, veh in enumerate(vehicles_1E5_1W5):
            if (veh.getPosition().x + veh.getSpeed().x,
                veh.getPosition().y + veh.getSpeed().y) in self.collision_check_E:
                draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                for j in range(-10, 11):
                    self.collision_check_E.append((veh.getPosition().x + j, veh.getPosition().y))
            else:
                if 336 <= veh.getPosition().x and veh.getPosition().x + veh.getSpeed().x < 335:
                    if self.propose((veh.getPosition().x, veh.getPosition().y), self.t_t,
                                    self.sendData_2["vehicle"][i + 8], 0):
                    # if True:
                        print(i+8, self.t_t, 'True')
                        veh.getPosition().x += veh.getSpeed().x

                        if veh.getPosition().x < 0:
                            veh.getPosition().x = 600

                        qp.drawPoint(veh.getPosition().x + 1, veh.getPosition().y - 1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_E.append(
                                (veh.getPosition().x + j, veh.getPosition().y))
                    else:
                        print(i + 8, self.t_t, 'False')
                        print(veh.getPosition().x, veh.getPosition().y)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_E.append(
                                (veh.getPosition().x + j, veh.getPosition().y))

                else:
                    veh.getPosition().x += veh.getSpeed().x

                    if veh.getPosition().x < 0:
                        veh.getPosition().x = 600

                    draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                    for j in range(-10, 11):
                        self.collision_check_E.append((veh.getPosition().x + j, veh.getPosition().y))

        # Vehicles Pattern1-1(from 1N5 to 1W5)
        for i, veh in enumerate(vehicles_1N5_1W5):
            # Check if there are vehicles ahead. If true, stop
            if (veh.getPosition().x + veh.getSpeed().x, veh.getPosition().y + veh.getSpeed().y) in self.collision_check_N:
                self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y, veh.getPosition().x,
                                      veh.getPosition().y, self.sendData_1)
                draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                # Make the room not available for other vehicles
                for j in range(-10, 11):
                    self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y + j))
            # Move forward
            else:
                # Just before the intersection
                if veh.getPosition().y == 264:
                    # Try to make a reservation
                    if self.propose((veh.getPosition().x, veh.getPosition().y), self.t_t, self.sendData_1["vehicle"][i], 0):
                        veh.getPosition().y += 1
                        print('Success')
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y,
                                              self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y + j))
                    # Not Enter intersection
                    else:
                        print('Failure')
                        self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_W.append((veh.getPosition().x, veh.getPosition().y + j))

                else:
                    # Already in the intersection
                    if 265 <= veh.getPosition().y < 315 and veh.getPosition().x > 265:

                        # Calculate trajectory by using Bezier Curve
                        x = pow(1 - (self.N5_1W5_beze_t[i] / 50), 2) * 315 + 2 * (self.N5_1W5_beze_t[i] / 50) * (
                        1 - self.N5_1W5_beze_t[i] / 50) * 315 + pow(
                            self.N5_1W5_beze_t[i] / 50, 2) * 265
                        y = pow(1 - (self.N5_1W5_beze_t[i] / 50), 2) * 265 + 2 * (self.N5_1W5_beze_t[i] / 50) * (
                        1 - self.N5_1W5_beze_t[i] / 50) * 315 + pow(
                            self.N5_1W5_beze_t[i] / 50, 2) * 315
                        veh.setPosition(Position(x, y))

                        self.N5_1W5_beze_t[i] += 2

                        if 15.0 < ((veh.getPosition().y - 265 + veh.getSpeed().y) / 50) * 90 <= 90.0:
                            self.N5_1W5_r[i] = ((veh.getPosition().y - 265 + veh.getSpeed().y) / 50) * 90
                        elif ((veh.getPosition().y - 265 + veh.getSpeed().y) / 50) * 90 > 90:
                            self.N5_1W5_r[i] = 90
                        else:
                            self.N5_1W5_r[i] = 0

                        # Influential veh_num calculation
                        self.calculate_vehnum_inside(i, self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, self.N5_1W5_r[i])
                        for j in range(-10, 11):
                            self.collision_check_W.append((veh.getPosition().x, veh.getPosition().y + j))

                    # Already left intersection
                    elif 315 <= veh.getPosition().y and veh.getPosition().x > 0:

                        veh.getPosition().x -= veh.getSpeed().y

                        # Influential veh_num calculation
                        old_x = veh.getPosition().x
                        old_y = veh.getPosition().y - veh.getSpeed().x
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y, sendData_1)

                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 90)
                        for j in range(-10, 11):
                            self.collision_check_W.append((veh.getPosition().x + j, veh.getPosition().y))
                        # qp.restore()

                    # Already left screen
                    elif veh.getPosition().x < 0:
                        veh.getPosition().x = 315
                        veh.getPosition().y = 0
                        self.N5_1W5_beze_t[i] = 2
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y, self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_W.append((veh.getPosition().x + j, veh.getPosition().y))

                    # Move vertical direction(across X_axis)
                    else:
                        veh.getPosition().y += veh.getSpeed().y
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y, self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y + j))



        # Vehicles Pattern1-2(from 1S2 to 1E2)
        for i, veh in enumerate(vehicles_1S2_1E2):
            # Check if there are vehicles ahead. If true, stop
            if (veh.getPosition().x + veh.getSpeed().x,
                veh.getPosition().y + veh.getSpeed().y) in self.collision_check_S:
                self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y, veh.getPosition().x,
                                      veh.getPosition().y, self.sendData_1)
                draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                # Make the room not available for other vehicles
                for j in range(-10, 11):
                    self.collision_check_S.append((veh.getPosition().x, veh.getPosition().y + j))
            # Move forward
            else:
                # Just before the intersection
                if veh.getPosition().y == 336:
                    # Try to make a reservation
                    if self.propose((veh.getPosition().x, veh.getPosition().y), self.t_t,
                                    self.sendData_1["vehicle"][i+2], 0):
                        veh.getPosition().y -= 1
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y,
                                              self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_S.append(
                                (veh.getPosition().x, veh.getPosition().y + j))
                    # Enter intersection
                    else:
                        self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y,
                                              veh.getPosition().x,veh.getPosition().y, self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_S.append(
                                (veh.getPosition().x, veh.getPosition().y + j))

                else:
                    # Already in the intersection
                    if 285 < veh.getPosition().y < 335 and veh.getPosition().x < 335:

                        # Calculate trajectory by using Bezier Curve
                        x = pow(1 - (self.S2_1E2_beze_t[i] / 50), 2) * 285 + 2 * (
                        self.S2_1E2_beze_t[i] / 50) * (1 - self.S2_1E2_beze_t[i] / 50) * 285 + pow(
                            self.S2_1E2_beze_t[i] / 50, 2) * 335
                        y = pow(1 - (self.S2_1E2_beze_t[i] / 50), 2) * 335 + 2 * (
                        self.S2_1E2_beze_t[i] / 50) * (1 - self.S2_1E2_beze_t[i] / 50) * 285 + pow(
                            self.S2_1E2_beze_t[i] / 50, 2) * 285
                        veh.setPosition(Position(x, y))

                        self.S2_1E2_beze_t[i] += 2

                        if 15.0 < ((335 - veh.getPosition().y + veh.getSpeed().y) / 50) * 90 <= 90.0:
                            self.S2_1E2_r[i] = ((335 - veh.getPosition().y + veh.getSpeed().y) / 50) * 90
                        elif ((335 - veh.getPosition().y + veh.getSpeed().y) / 50) * 90 > 90:
                            self.S2_1E2_r[i] = 90
                        else:
                            self.S2_1E2_r[i] = 0

                        # Influential veh_num calculation
                        self.calculate_vehnum_inside(i, self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y,
                                           self.S2_1E2_r[i])
                        for j in range(-10, 11):
                            self.collision_check_S.append(
                                (veh.getPosition().x, veh.getPosition().y + j))

                    # Already left intersection
                    elif 285 >= veh.getPosition().y and veh.getPosition().x >= 335:

                        veh.getPosition().x -= veh.getSpeed().y

                        # Influential veh_num calculation
                        old_x = veh.getPosition().x
                        old_y = veh.getPosition().y - veh.getSpeed().x
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y,
                                              sendData_1)

                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 90)
                        for j in range(-10, 11):
                            self.collision_check_S.append(
                                (veh.getPosition().x + j, veh.getPosition().y))
                            # qp.restore()

                    # Already left screen
                    elif veh.getPosition().x > 600:
                        veh.getPosition().x = 285
                        veh.getPosition().y = 600
                        self.S2_1E2_beze_t[i] = 2
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y,
                                              self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_S.append(
                                (veh.getPosition().x + j, veh.getPosition().y))

                    # Move vertical direction(across X_axis)
                    else:
                        veh.getPosition().y += veh.getSpeed().y
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x, veh.getPosition().y,
                                              self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_S.append(
                                (veh.getPosition().x, veh.getPosition().y + j))

        # Vehicles Pattern1-3(from W2 to S5)
        for i, veh in enumerate(vehicles_W_S):
            # Check if there are vehicles ahead. If true, stop
            if (veh.getPosition().x + veh.getSpeed().x,
                veh.getPosition().y + veh.getSpeed().y) in self.collision_check_W:
                self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y,
                                      veh.getPosition().x,veh.getPosition().y, self.sendData_1)
                draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                # Make the room not available for other vehicles
                for j in range(-10, 11):
                    self.collision_check_W.append((veh.getPosition().x + j, veh.getPosition().y))
            # Move forward
            else:
                # Just before the intersection
                if veh.getPosition().x == 264:
                    # Try to make a reservation
                    if self.propose((veh.getPosition().x, veh.getPosition().y), self.t_t,
                                    self.sendData_1["vehicle"][i+4], 0):
                        veh.getPosition().x += 1
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y,self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_W.append((veh.getPosition().x + j, veh.getPosition().y))
                    # Enter intersection
                    else:
                        self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y,
                                              veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_W.append(
                                (veh.getPosition().x + j, veh.getPosition().y))

                else:
                    # Already in the intersection
                    if 265 <= veh.getPosition().x <= 315 and veh.getPosition().y < 335:

                        # Calculate trajectory by using Bezier Curve
                        x = pow(1 - (self.beze_t[i] / 50), 2) * 265 + 2 * (self.beze_t[i] / 50) * (
                            1 - self.beze_t[i] / 50) * 315 + pow(
                            self.beze_t[i] / 50, 2) * 315
                        y = pow(1 - (self.beze_t[i] / 50), 2) * 285 + 2 * (self.beze_t[i] / 50) * (
                            1 - self.beze_t[i] / 50) * 285 + pow(
                            self.beze_t[i] / 50, 2) * 335
                        veh.setPosition(Position(x, y))

                        self.beze_t[i] += 2

                        if 15.0 < ((veh.getPosition().x - 265 + veh.getSpeed().x) / 50) * 90 <= 90.0:
                            self.r[i] = ((veh.getPosition().x - 265 + veh.getSpeed().x) / 50) * 90
                        elif ((veh.getPosition().x - 265 + veh.getSpeed().x) / 50) * 90 > 90:
                            self.r[i] = 90
                        else:
                            self.r[i] = 0

                        # Influential veh_num calculation
                        self.calculate_vehnum_inside(i, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, self.r[i])
                        for j in range(-10, 11):
                            self.collision_check_W.append((veh.getPosition().x + j, veh.getPosition().y))

                    # Already left intersection
                    elif 315 <= veh.getPosition().x and veh.getPosition().y < 600:

                        veh.getPosition().y += veh.getSpeed().x

                        # Influential veh_num calculation
                        old_x = veh.getPosition().x
                        old_y = veh.getPosition().y - veh.getSpeed().x
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, sendData_1)

                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 90)
                        for j in range(-10, 11):
                            self.collision_check_W.append((veh.getPosition().x, veh.getPosition().y + j))
                            # qp.restore()

                    # Already left screen
                    elif veh.getPosition().y >= 600:
                        veh.getPosition().x = 0
                        veh.getPosition().y = 285
                        self.beze_t[i] = 2
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_W.append(
                                (veh.getPosition().x, veh.getPosition().y + j))

                    # Move horizontal direction(across X_axis)
                    else:
                        veh.getPosition().x += veh.getSpeed().x
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_W.append(
                                (veh.getPosition().x + j, veh.getPosition().y))

        # Vehicles Pattern1-4(from 1E5 to 1N2)
        for i, veh in enumerate(vehicles_1E5_1N2):
            # Check if there are vehicles ahead. If true, stop
            if (veh.getPosition().x + veh.getSpeed().x,
                veh.getPosition().y + veh.getSpeed().y) in self.collision_check_E:
                self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y,
                                      veh.getPosition().x,
                                      veh.getPosition().y, self.sendData_1)
                draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                # Make the room not available for other vehicles
                for j in range(-10, 11):
                    self.collision_check_E.append((veh.getPosition().x + j, veh.getPosition().y))
            # Move forward
            else:
                # Just before the intersection
                if veh.getPosition().x == 336:
                    # Try to make a reservation
                    if self.propose((veh.getPosition().x, veh.getPosition().y), self.t_t,
                                    self.sendData_1["vehicle"][i + 6], 0):
                    # if True:
                        veh.getPosition().x -= 1
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y,
                                              self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_E.append(
                                (veh.getPosition().x + j, veh.getPosition().y))
                    # Enter intersection
                    else:
                        self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y,
                                              veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_E.append(
                                (veh.getPosition().x + j, veh.getPosition().y))

                else:
                    # Already in the intersection
                    if 285 < veh.getPosition().x <= 335 and veh.getPosition().y > 265:

                        # Calculate trajectory by using Bezier Curve
                        x = pow(1 - (self.E5_1N2_beze_t[i] / 50), 2) * 335 + 2 * (self.E5_1N2_beze_t[i] / 50) * (
                            1 - self.E5_1N2_beze_t[i] / 50) * 285 + pow(
                            self.E5_1N2_beze_t[i] / 50, 2) * 285
                        y = pow(1 - (self.E5_1N2_beze_t[i] / 50), 2) * 315 + 2 * (self.E5_1N2_beze_t[i] / 50) * (
                            1 - self.E5_1N2_beze_t[i] / 50) * 315 + pow(
                            self.E5_1N2_beze_t[i] / 50, 2) * 265
                        veh.setPosition(Position(x, y))

                        self.E5_1N2_beze_t[i] += 2

                        if 15.0 < ((335 - veh.getPosition().x + veh.getSpeed().x) / 50) * 90 <= 90.0:
                            self.E5_1N2_r[i] = ((335 - veh.getPosition().x + veh.getSpeed().x) / 50) * 90
                        elif ((335 - veh.getPosition().x + veh.getSpeed().x) / 50) * 90 > 90:
                            self.E5_1N2_r[i] = 90
                        else:
                            self.E5_1N2_r[i] = 0

                        # Influential veh_num calculation
                        self.calculate_vehnum_inside(i, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, self.E5_1N2_r[i])
                        for j in range(-10, 11):
                            self.collision_check_E.append(
                                (veh.getPosition().x + j, veh.getPosition().y))

                    # Already left intersection
                    elif 285 >= veh.getPosition().x and veh.getPosition().y <= 265:

                        veh.getPosition().y += veh.getSpeed().x

                        # Influential veh_num calculation
                        old_x = veh.getPosition().x
                        old_y = veh.getPosition().y - veh.getSpeed().x
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, sendData_1)

                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 90)
                        for j in range(-10, 11):
                            self.collision_check_E.append(
                                (veh.getPosition().x, veh.getPosition().y + j))
                            # qp.restore()

                    # Already left screen
                    elif veh.getPosition().y <= 0:
                        veh.getPosition().x = 600
                        veh.getPosition().y = 315
                        self.E5_1N2_beze_t[i] = 2
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_E.append(
                                (veh.getPosition().x, veh.getPosition().y + j))

                    # Move horizontal direction(across X_axis)
                    else:
                        veh.getPosition().x += veh.getSpeed().x
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_E.append(
                                (veh.getPosition().x + j, veh.getPosition().y))

    # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


        # Vehicles Pattern3-1(from 1N5 to 1E2)
        for i, veh in enumerate(vehicles_1N5_1E2):
            # Check if there are vehicles ahead. If true, stop
            if (veh.getPosition().x + veh.getSpeed().x,
                veh.getPosition().y + veh.getSpeed().y) in self.collision_check_N:
                self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y,
                                      veh.getPosition().x,
                                      veh.getPosition().y, self.sendData_1)
                draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                # Make the room not available for other vehicles
                for j in range(-10, 11):
                    self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y + j))
            # Move forward
            else:
                # Just before the intersection
                if veh.getPosition().y == 264:
                    # Try to make a reservation
                    if self.propose((veh.getPosition().x, veh.getPosition().y), self.t_t,self.sendData_3["vehicle"][i], 0):
                        veh.getPosition().y += 1
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,veh.getPosition().y,self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_N.append(
                                (veh.getPosition().x, veh.getPosition().y + j))
                    # Enter intersection
                    else:
                        self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y,veh.getPosition().x,veh.getPosition().y, self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y + j))

                else:
                    # Already in the intersection
                    if 265 < veh.getPosition().y < 285 and veh.getPosition().x < 335:

                        # Calculate trajectory by using Bezier Curve
                        x = pow(1 - (self.N5_1E2_beze_t[i] / 20), 2) * 315 + 2 * (
                        self.N5_1E2_beze_t[i] / 20) * (1 - self.N5_1E2_beze_t[i] / 20) * 315 + pow(
                            self.N5_1E2_beze_t[i] / 20, 2) * 335
                        y = pow(1 - (self.N5_1E2_beze_t[i] / 20), 2) * 265 + 2 * (
                        self.N5_1E2_beze_t[i] / 20) * (1 - self.N5_1E2_beze_t[i] / 20) * 285 + pow(
                            self.N5_1E2_beze_t[i] / 20, 2) * 285
                        veh.setPosition(Position(x, y))

                        self.N5_1E2_beze_t[i] += 2

                        if 15.0 < ((veh.getPosition().y - 265 + veh.getSpeed().y) / 20) * 90 <= 90.0:
                            self.N5_1E2_r[i] = -((veh.getPosition().y - 265 + veh.getSpeed().y) / 20) * 90
                        elif ((veh.getPosition().y - 265 + veh.getSpeed().y) / 20) * 90 > 90:
                            self.N5_1E2_r[i] = -90
                        else:
                            self.N5_1E2_r[i] = 0

                        # Influential veh_num calculation
                        self.calculate_vehnum_inside(i, self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y,
                                           self.N5_1E2_r[i])
                        for j in range(-10, 11):
                            self.collision_check_N.append(
                                (veh.getPosition().x, veh.getPosition().y + j))

                    # Already left intersection
                    elif 285 <= veh.getPosition().y and veh.getPosition().x <= 600:

                        veh.getPosition().x += veh.getSpeed().y

                        # Influential veh_num calculation
                        old_x = veh.getPosition().x
                        old_y = veh.getPosition().y - veh.getSpeed().x
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, sendData_1)

                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, -90)
                        for j in range(-10, 11):
                            self.collision_check_N.append(
                                (veh.getPosition().x + j, veh.getPosition().y))
                            # qp.restore()

                    # Already left screen
                    elif veh.getPosition().x > 600:
                        veh.getPosition().x = 315
                        veh.getPosition().y = 0
                        self.N5_1E2_beze_t[i] = 2
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_N.append(
                                (veh.getPosition().x + j, veh.getPosition().y))

                    # Move vertical direction(across X_axis)
                    else:
                        veh.getPosition().y += veh.getSpeed().y
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_N.append(
                                (veh.getPosition().x, veh.getPosition().y + j))


        # Vehicles Pattern3-2(from 1S2 to 1W5)
        for i, veh in enumerate(vehicles_1S2_1W5):
            # Check if there are vehicles ahead. If true, stop
            if (veh.getPosition().x + veh.getSpeed().x,
                veh.getPosition().y + veh.getSpeed().y) in self.collision_check_S:
                self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y,
                                      veh.getPosition().x,
                                      veh.getPosition().y, self.sendData_1)
                draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                # Make the room not available for other vehicles
                for j in range(-10, 11):
                    self.collision_check_S.append((veh.getPosition().x, veh.getPosition().y + j))
            # Move forward
            else:
                # Just before the intersection
                if veh.getPosition().y == 336:
                    # Try to make a reservation
                    if self.propose((veh.getPosition().x, veh.getPosition().y), self.t_t,
                                    self.sendData_3["vehicle"][i+2], 0):
                        veh.getPosition().y -= 1
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_S.append(
                                (veh.getPosition().x, veh.getPosition().y + j))
                    # Enter intersection
                    else:
                        self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y,
                                              veh.getPosition().x, veh.getPosition().y,
                                              self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_S.append(
                                (veh.getPosition().x, veh.getPosition().y + j))

                else:
                    # Already in the intersection
                    if 315 < veh.getPosition().y < 335 and veh.getPosition().x <= 285:

                        # Calculate trajectory by using Bezier Curve
                        x = pow(1 - (self.S2_1W5_beze_t[i] / 20), 2) * 285 + 2 * (
                            self.S2_1W5_beze_t[i] / 20) * (1 - self.S2_1W5_beze_t[
                            i] / 20) * 285 + pow(self.S2_1W5_beze_t[i] / 20, 2) * 265
                        y = pow(1 - (self.S2_1W5_beze_t[i] / 20), 2) * 335 + 2 * (
                            self.S2_1W5_beze_t[i] / 20) * (1 - self.S2_1W5_beze_t[
                            i] / 20) * 315 + pow(self.S2_1W5_beze_t[i] / 20, 2) * 315
                        veh.setPosition(Position(x, y))

                        self.S2_1W5_beze_t[i] += 2

                        if 15.0 < ((335 - (veh.getPosition().y + veh.getSpeed().y)) / 20) * 90 < 90.0:
                            self.S2_1W5_r[i] = -((335 - (veh.getPosition().y + veh.getSpeed().y)) / 20) * 90
                        elif ((335 - (veh.getPosition().y + veh.getSpeed().y)) / 20) * 90 > 90:
                            self.S2_1W5_r[i] = -90
                        else:
                            self.S2_1W5_r[i] = 0

                        # Influential veh_num calculation
                        self.calculate_vehnum_inside(i, self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y,
                                           self.S2_1W5_r[i])
                        for j in range(-10, 11):
                            self.collision_check_S.append(
                                (veh.getPosition().x, veh.getPosition().y + j))

                    # Already left intersection
                    elif 315 >= veh.getPosition().y and veh.getPosition().x >= 0:

                        veh.getPosition().x += veh.getSpeed().y

                        # Influential veh_num calculation
                        old_x = veh.getPosition().x
                        old_y = veh.getPosition().y - veh.getSpeed().x
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, sendData_1)

                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, -90)
                        for j in range(-10, 11):
                            self.collision_check_S.append(
                                (veh.getPosition().x + j, veh.getPosition().y))
                            # qp.restore()

                    # Already left screen
                    elif veh.getPosition().x < 0:
                        veh.getPosition().x = 285
                        veh.getPosition().y = 600
                        self.S2_1W5_beze_t[i] = 2
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_S.append(
                                (veh.getPosition().x + j, veh.getPosition().y))

                    # Move vertical direction(across X_axis)
                    else:
                        veh.getPosition().y += veh.getSpeed().y
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_v_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_S.append(
                                (veh.getPosition().x, veh.getPosition().y + j))

        # Vehicles Pattern3-3(from W2 to N2)
        for i, veh in enumerate(vehicles_1W2_1N2):
            # Check if there are vehicles ahead. If true, stop
            if (veh.getPosition().x + veh.getSpeed().x,
                veh.getPosition().y + veh.getSpeed().y) in self.collision_check_W:
                self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y,
                                      veh.getPosition().x,
                                      veh.getPosition().y, self.sendData_1)
                draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                # Make the room not available for other vehicles
                for j in range(-10, 11):
                    self.collision_check_W.append((veh.getPosition().x + j, veh.getPosition().y))
            # Move forward
            else:
                # Just before the intersection
                if veh.getPosition().x == 264:
                    # Try to make a reservation
                    if self.propose((veh.getPosition().x, veh.getPosition().y), self.t_t,
                                    self.sendData_3["vehicle"][i + 4], 0):
                        veh.getPosition().x += 1
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y,
                                              self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_W.append(
                                (veh.getPosition().x + j, veh.getPosition().y))
                    # Enter intersection
                    else:
                        self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y,
                                              veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_W.append(
                                (veh.getPosition().x + j, veh.getPosition().y))

                else:
                    # Already in the intersection
                    if 265 < veh.getPosition().x and 265 < veh.getPosition().y <= 285:

                        # Calculate trajectory by using Bezier Curve
                        x = pow(1 - (self.W2_1N2_beze_t[i] / 20), 2) * 265 + 2 * (self.W2_1N2_beze_t[i] / 20) * (
                            1 - self.W2_1N2_beze_t[i] / 20) * 285 + pow(
                            self.W2_1N2_beze_t[i] / 20, 2) * 285
                        y = pow(1 - (self.W2_1N2_beze_t[i] / 20), 2) * 285 + 2 * (self.W2_1N2_beze_t[i] / 20) * (
                            1 - self.W2_1N2_beze_t[i] / 20) * 285 + pow(
                            self.W2_1N2_beze_t[i] / 20, 2) * 265
                        veh.setPosition(Position(x, y))

                        self.W2_1N2_beze_t[i] += 2

                        if 15.0 < ((veh.getPosition().x - 265 + veh.getSpeed().x) / 20) * 90 <= 90.0:
                            self.W2_1N2_r[i] = -((veh.getPosition().x - 265 + veh.getSpeed().x) / 20) * 90
                        elif ((veh.getPosition().x - 265 + veh.getSpeed().x) / 20) * 90 > 90:
                            self.W2_1N2_r[i] = -90
                        else:
                            self.W2_1N2_r[i] = 0

                        # Influential veh_num calculation
                        self.calculate_vehnum_inside(i, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, self.W2_1N2_r[i])
                        for j in range(-10, 11):
                            self.collision_check_W.append(
                                (veh.getPosition().x + j, veh.getPosition().y))

                    # Already left intersection
                    elif 285 <= veh.getPosition().x and veh.getPosition().y > 0:

                        veh.getPosition().y -= veh.getSpeed().x

                        # Influential veh_num calculation
                        old_x = veh.getPosition().x
                        old_y = veh.getPosition().y - veh.getSpeed().x
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, sendData_1)

                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, -90)
                        for j in range(-10, 11):
                            self.collision_check_W.append(
                                (veh.getPosition().x, veh.getPosition().y + j))
                            # qp.restore()

                    # Already left screen
                    elif veh.getPosition().y <= 0:
                        veh.getPosition().x = 0
                        veh.getPosition().y = 285
                        self.W2_1N2_beze_t[i] = 2
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_W.append(
                                (veh.getPosition().x, veh.getPosition().y + j))

                    # Move horizontal direction(across X_axis)
                    else:
                        veh.getPosition().x += veh.getSpeed().x
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_W.append(
                                (veh.getPosition().x + j, veh.getPosition().y))

        # Vehicles Pattern3-4(from 1E5 to 1S5)
        for i, veh in enumerate(vehicles_1E5_1S5):
            # Check if there are vehicles ahead. If true, stop
            if (veh.getPosition().x + veh.getSpeed().x,
                veh.getPosition().y + veh.getSpeed().y) in self.collision_check_E:
                self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y,
                                      veh.getPosition().x,
                                      veh.getPosition().y, self.sendData_1)
                draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                # Make the room not available for other vehicles
                for j in range(-10, 11):
                    self.collision_check_E.append((veh.getPosition().x + j, veh.getPosition().y))
            # Move forward
            else:
                # Just before the intersection
                if veh.getPosition().x == 336:
                    # Try to make a reservation
                    if self.propose((veh.getPosition().x, veh.getPosition().y), self.t_t,
                                    self.sendData_3["vehicle"][i + 6], 0):
                    # if True:
                        veh.getPosition().x -= 1
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y,
                                              self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_E.append(
                                (veh.getPosition().x + j, veh.getPosition().y))
                    # Enter intersection
                    else:
                        self.calculate_vehnum(i, veh.getPosition().x, veh.getPosition().y,
                                              veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_E.append(
                                (veh.getPosition().x + j, veh.getPosition().y))

                else:
                    # Already in the intersection
                    if 315 <= veh.getPosition().x < 335 and 315 <= veh.getPosition().y < 335:

                        # Calculate trajectory by using Bezier Curve
                        x = pow(1 - (self.E5_1S5_beze_t[i] / 20), 2) * 335 + 2 * (
                        self.E5_1S5_beze_t[i] / 20) * (1 - self.E5_1S5_beze_t[i] / 20) * 315 + pow(
                            self.E5_1S5_beze_t[i] / 20, 2) * 315
                        y = pow(1 - (self.E5_1S5_beze_t[i] / 20), 2) * 315 + 2 * (
                        self.E5_1S5_beze_t[i] / 20) * (1 - self.E5_1S5_beze_t[i] / 20) * 315 + pow(
                            self.E5_1S5_beze_t[i] / 20, 2) * 335
                        veh.setPosition(Position(x, y))

                        self.E5_1S5_beze_t[i] += 2

                        if 15.0 < ((335 - veh.getPosition().x + veh.getSpeed().x) / 20) * 90 <= 90.0:
                            self.E5_1S5_r[i] = -((335 - veh.getPosition().x + veh.getSpeed().x) / 20) * 90
                        elif ((335 - veh.getPosition().x + veh.getSpeed().x) / 20) * 90 > 90:
                            self.E5_1S5_r[i] = -90
                        else:
                            self.E5_1S5_r[i] = 0

                        # Influential veh_num calculation
                        self.calculate_vehnum_inside(i, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y,
                                           self.E5_1S5_r[i])
                        for j in range(-10, 11):
                            self.collision_check_E.append(
                                (veh.getPosition().x + j, veh.getPosition().y))

                    # Already left intersection
                    elif 315 <= veh.getPosition().x and veh.getPosition().y >= 335:

                        veh.getPosition().y -= veh.getSpeed().x

                        # Influential veh_num calculation
                        old_x = veh.getPosition().x
                        old_y = veh.getPosition().y - veh.getSpeed().x
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, sendData_1)

                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, -90)
                        for j in range(-10, 11):
                            self.collision_check_E.append(
                                (veh.getPosition().x, veh.getPosition().y + j))
                            # qp.restore()

                    # Already left screen
                    elif veh.getPosition().y >= 600:
                        veh.getPosition().x = 600
                        veh.getPosition().y = 315
                        self.E5_1S5_beze_t[i] = 2
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_E.append(
                                (veh.getPosition().x, veh.getPosition().y + j))

                    # Move horizontal direction(across X_axis)
                    else:
                        veh.getPosition().x += veh.getSpeed().x
                        # Influential veh_num calculation
                        old_x = veh.getPosition().x - veh.getSpeed().x
                        old_y = veh.getPosition().y - veh.getSpeed().y
                        self.calculate_vehnum(i, old_x, old_y, veh.getPosition().x,
                                              veh.getPosition().y, self.sendData_1)
                        draw_veh.new_t_rec(qp, veh.getPosition().x, veh.getPosition().y, 0)
                        for j in range(-10, 11):
                            self.collision_check_E.append(
                                (veh.getPosition().x + j, veh.getPosition().y))




            self.collision_check = []
            self.collision_check_N = []
            self.collision_check_S = []
            self.collision_check_W = []
            self.collision_check_E = []
            self.collision_check_N2 = []

            self.ti += 10
            if self.ti > 700:
                self.ti = 0
                # print(self.t.elapsed())
                self.t.restart()

        # print("*********************")
        # print(self.intersec1_vehnum)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # ***************************************************
    # Vehicles from 1North5 to 1South5
    vehicles_1N5_1S5 = []
    # for i in range(5):
    #     v = Vehicle()
    #     v.setPosition(Position(313, 0 - i * 20))
    #     v.setSpeed(Speed(0, 2))
    #     v.setSize(Size(5, 10))
    #     vehicles_1N5_1S5.append(v)
    v = Vehicle()
    v.setPosition(Position(315, 0))
    v.setSpeed(Speed(0, 2))
    v.setSize(Size(5, 10))
    vehicles_1N5_1S5.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(315, 0 - 2 * 40))
    # v.setSpeed(Speed(0, 2))
    # v.setSize(Size(5, 10))
    # vehicles_1N5_1S5.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(315, 0 - 2 * 60))
    # v.setSpeed(Speed(0, 2))
    # v.setSize(Size(5, 10))
    # vehicles_1N5_1S5.append(v)

    # ***************************************************
    # Vehicles from 1South2 to 1North2
    vehicles_1S2_1N2 = []
    v = Vehicle()
    v.setPosition(Position(285, 600))
    v.setSpeed(Speed(0, -2))
    v.setSize(Size(5, 10))
    vehicles_1S2_1N2.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(285, 600 + 2 * 40))
    # v.setSpeed(Speed(0, -2))
    # v.setSize(Size(5, 10))
    # vehicles_1S2_1N2.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(285, 600 + 2 * 60))
    # v.setSpeed(Speed(0, -2))
    # v.setSize(Size(5, 10))
    # vehicles_1S2_1N2.append(v)

    # ***************************************************
    # Vehicles from 1W2 to 1E2
    vehicles_1W2_1E2 = []
    v = Vehicle()
    v.setPosition(Position(0, 285))
    v.setSpeed(Speed(2, 0))
    v.setSize(Size(10, 5))
    vehicles_1W2_1E2.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(0 - 2 * 80, 285))
    # v.setSpeed(Speed(2, 0))
    # v.setSize(Size(10, 5))
    # vehicles_1W2_1E2.append(v)

    # ***************************************************
    # Vehicles from 1E5 to 1W5
    vehicles_1E5_1W5 = []
    v = Vehicle()
    v.setPosition(Position(600, 315))
    v.setSpeed(Speed(-2, 0))
    v.setSize(Size(10, 5))
    vehicles_1E5_1W5.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(600 + 2 * 80, 315))
    # v.setSpeed(Speed(-2, 0))
    # v.setSize(Size(10, 5))
    # vehicles_1E5_1W5.append(v)


    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ***************************************************
    # Vehicles from 1N5 to 1W5
    vehicles_1N5_1W5 = []
    v = Vehicle()
    v.setPosition(Position(315, 0 - 50))
    v.setSpeed(Speed(0, 2))
    v.setSize(Size(10, 5))
    vehicles_1N5_1W5.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(315, 0 - 30))
    # v.setSpeed(Speed(0, 2))
    # v.setSize(Size(10, 5))
    # vehicles_1N5_1W5.append(v)

    # ***************************************************
    # Vehicles from 1S2 to 1E2
    vehicles_1S2_1E2 = []
    v = Vehicle()
    v.setPosition(Position(285, 600 + 50))
    v.setSpeed(Speed(0, -2))
    v.setSize(Size(10, 5))
    vehicles_1S2_1E2.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(285, 600 + 30))
    # v.setSpeed(Speed(0, -2))
    # v.setSize(Size(10, 5))
    # vehicles_1S2_1E2.append(v)

    # ***************************************************
    # Vehicles from West1 to South6
    vehicles_W_S = []
    v = Vehicle()
    v.setPosition(Position(0 - 50, 285))
    v.setSpeed(Speed(2, 0))
    v.setSize(Size(10, 5))
    vehicles_W_S.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(0 - 2 * 100, 285))
    # v.setSpeed(Speed(2, 0))
    # v.setSize(Size(10, 5))
    # vehicles_W_S.append(v)

    # ***************************************************
    # Vehicles from West1 to South6
    vehicles_1E5_1N2 = []
    v = Vehicle()
    v.setPosition(Position(600 + 50, 315))
    v.setSpeed(Speed(-2, 0))
    v.setSize(Size(10, 5))
    vehicles_1E5_1N2.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(600 + 2 * 100, 315))
    # v.setSpeed(Speed(-2, 0))
    # v.setSize(Size(10, 5))
    # vehicles_1E5_1N2.append(v)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ***************************************************
    # Vehicles from 1N5 to 1E2
    vehicles_1N5_1E2 = []
    v = Vehicle()
    v.setPosition(Position(315, 0 - 200))
    v.setSpeed(Speed(0, 2))
    v.setSize(Size(5, 10))
    vehicles_1N5_1E2.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(315, 0 - 2 * 50))
    # v.setSpeed(Speed(0, 2))
    # v.setSize(Size(5, 10))
    # vehicles_1N5_1E2.append(v)

    # ***************************************************
    # Vehicles from 1S2 to 1W5
    vehicles_1S2_1W5 = []
    v = Vehicle()
    v.setPosition(Position(285, 600 + 100))
    v.setSpeed(Speed(0, -2))
    v.setSize(Size(5, 10))
    vehicles_1S2_1W5.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(285, 600 + 2 * 50))
    # v.setSpeed(Speed(0, -2))
    # v.setSize(Size(5, 10))
    # vehicles_1S2_1W5.append(v)

    # ***************************************************
    # Vehicles from 1S2 to 1W5
    vehicles_1W2_1N2 = []
    v = Vehicle()
    v.setPosition(Position(0 - 100, 285))
    v.setSpeed(Speed(2, 0))
    v.setSize(Size(5, 10))
    vehicles_1W2_1N2.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(0 - 100, 285))
    # v.setSpeed(Speed(2, 0))
    # v.setSize(Size(5, 10))
    # vehicles_1W2_1N2.append(v)

    # ***************************************************
    # Vehicles from 1E5 to 1S5
    vehicles_1E5_1S5 = []
    v = Vehicle()
    v.setPosition(Position(600 + 100, 315))
    v.setSpeed(Speed(-2, 0))
    v.setSize(Size(5, 10))
    vehicles_1E5_1S5.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(600 + 100, 315))
    # v.setSpeed(Speed(-2, 0))
    # v.setSize(Size(5, 10))
    # vehicles_1E5_1S5.append(v)




    # Read vehicles info from json file
    f = open('veh_info/veh.json', 'r')
    sendData_1 = json.load(f)
    f.close()

    f = open('veh_info/veh_2.json', 'r')
    sendData_2 = json.load(f)
    f.close()

    f = open('veh_info/veh_3.json', 'r')
    sendData_3 = json.load(f)
    f.close()

    f = open('veh_info/veh_4.json', 'r')
    sendData_4 = json.load(f)
    f.close()

    f = open('veh_info/veh_5.json', 'r')
    sendData_5 = json.load(f)
    f.close()

    f = open('veh_info/veh_Ex1.json', 'r')
    sendData_Ex1 = json.load(f)
    f.close()

    f = open('veh_info/veh_6.json', 'r')
    sendData_6 = json.load(f)
    f.close()

    f = open('veh_info/veh_7.json', 'r')
    sendData_7 = json.load(f)
    f.close()

    f = open('veh_info/veh_8.json', 'r')
    sendData_8 = json.load(f)
    f.close()

    ex = Example(sendData_1, sendData_2, sendData_3, sendData_4, sendData_5, sendData_Ex1)

    sys.exit(app.exec_())