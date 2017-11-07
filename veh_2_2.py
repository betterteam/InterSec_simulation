# coding:utf-8
# Test vehicle with UDP
# Already has three travel patterns
# From 1027
# Try to make the source clean


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

sys.path.append('Users/better/PycharmProjects/GUI_Qt5/Intersection')
import rec_funcs

class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Speed:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Size:
    def __init__(self, x=5, y=10):
        self.x = x
        self.y = y

class Vehicle:
    def __init__(self):
        self._position = Position()
        self._speed = Speed()
        self._size = Size()

    def setPosition(self, position):
        self._position = position

    def getPosition(self):
        return self._position

    def setSpeed(self, speed):
        self._speed = speed

    def getSpeed(self):
        return self._speed

    def setSize(self, size):
        self._size = size

    def getSize(self):
        return self._size

    def moveNext(self):
        self._position.x += self._speed.x
        self._position.y += self._speed.y
        if self._position.x > 600:
            self._position.x = 0

class Example(QWidget):
    def __init__(self, vehicles_N, vehicles_W, vehicles_E, vehicles_S3_W4, sendData_1, sendData_2, sendData_3, sendData_4):
        super().__init__()
        self.vehicles_N = vehicles_N
        self.vehicles_W = vehicles_W
        self.vehicles_E = vehicles_E
        self.sendData_1 = sendData_1
        self.sendData_2 = sendData_2
        self.sendData_3 = sendData_3
        self.sendData_4 = sendData_4
        self.my_result = 0
        self.t_t = 0

        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000/60)#一秒間隔で更新

        self.t = QTime()
        self.t.start()
        self.show()

    def initUI(self):
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle("Koku's Simulation")

        self.ti = 0
        self.beze_t = []
        self.r = []
        self.up_left_x = []
        self.up_left_y = []
        self.down_left_x = []
        self.down_left_y = []
        self.up_right_x = []
        self.up_right_y = []
        self.down_right_x = []
        self.down_right_y = []

        self.S3_W4_beze_t = []
        self.S3_W4_r = []
        self.S3_W4_up_left_x = []
        self.S3_W4_up_left_y = []
        self.S3_W4_down_left_x = []
        self.S3_W4_down_left_y = []
        self.S3_W4_up_right_x = []
        self.S3_W4_up_right_y = []
        self.S3_W4_down_right_x = []
        self.S3_W4_down_right_y = []

        for i in range(10):
            self.beze_t.append(2)
            self.r.append(0)
            self.up_left_x.append(0)
            self.up_left_y.append(0)
            self.down_left_x.append(0)
            self.down_left_y.append(0)
            self.up_right_x.append(0)
            self.up_right_y.append(0)
            self.down_right_x.append(0)
            self.down_right_y.append(0)

            self.S3_W4_beze_t.append(0)
            self.S3_W4_r.append(0)
            self.S3_W4_up_left_x.append(0)
            self.S3_W4_up_left_y.append(0)
            self.S3_W4_down_left_x.append(0)
            self.S3_W4_down_left_y.append(0)
            self.S3_W4_up_right_x.append(0)
            self.S3_W4_up_right_y.append(0)
            self.S3_W4_down_right_x.append(0)
            self.S3_W4_down_right_y.append(0)



        self.single_0_0 = True
        self.single_0_1 = True

        self.collision_check = []
        self.collision_check_N = []
        self.collision_check_S = []
        self.collision_check_W = []
        self.collision_check_E = []


        self.grid = {}

        for i in range(270, 330, 10):
            for j in range(270, 330, 10):
                self.grid[(i, j)] = True

    def paintEvent(self, e):
        self.t_t += 1
        qp = QPainter(self)

        self.drawLines(qp)
        #self.drawSignals_0(qp)
        self.drawVehicles(qp)

    def drawLines(self, qp):

        # print(self.t.elapsed())

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        pen_dash = QPen(Qt.black, 2, Qt.DotLine)

        # Vertical
        qp.setPen(pen)
        qp.drawLine(270, 0, 270, 600)

        # with grids ##################
        # qp.drawLine(280, 0, 280, 600)
        # qp.drawLine(290, 0, 290, 600)
        # qp.drawLine(300, 0, 300, 600)
        # qp.drawLine(310, 0, 310, 600)
        # qp.drawLine(320, 0, 320, 600)
        # with grids ##################

        qp.drawLine(330, 0, 330, 600)
        qp.drawLine(300, 0, 300, 270)
        qp.drawLine(300, 330, 300, 600)

        qp.setPen(pen_dash)
        qp.drawLine(280, 330, 280, 600)
        qp.drawLine(290, 330, 290, 600)
        qp.drawLine(310, 330, 310, 600)
        qp.drawLine(320, 330, 320, 600)

        qp.drawLine(280, 0, 280, 270)
        qp.drawLine(290, 0, 290, 270)
        qp.drawLine(310, 0, 310, 270)
        qp.drawLine(320, 0, 320, 270)

        # Tropical
        qp.setPen(pen)
        qp.drawLine(0, 270, 600, 270)

        # with grids ##################
        # qp.drawLine(0, 280, 600, 280)
        # qp.drawLine(0, 290, 600, 290)
        # qp.drawLine(0, 300, 600, 300)
        # qp.drawLine(0, 310, 600, 310)
        # qp.drawLine(0, 320, 600, 320)
        # with grids ##################

        qp.drawLine(0, 330, 600, 330)
        qp.drawLine(0, 300, 270, 300)

        qp.drawLine(330, 300, 600, 300)

        qp.setPen(pen_dash)
        qp.drawLine(0, 280, 270, 280)
        qp.drawLine(0, 290, 270, 290)
        qp.drawLine(0, 310, 270, 310)
        qp.drawLine(0, 320, 270, 320)

        qp.drawLine(330, 280, 600, 280)
        qp.drawLine(330, 290, 600, 290)
        qp.drawLine(330, 310, 600, 310)
        qp.drawLine(330, 320, 600, 320)


    def drawSignals_0(self, qp):
        #print(self.t.elapsed())

        if 1000 < self.t.elapsed() < 2000:
            qp.setPen(Qt.black)
            qp.setBrush(Qt.red)

            qp.drawEllipse(272, 262, 6, 6)
            qp.drawEllipse(282, 262, 6, 6)
            qp.drawEllipse(292, 262, 6, 6)

            qp.setBrush(Qt.green)
            qp.drawEllipse(332, 272, 6, 6)
            qp.drawEllipse(332, 282, 6, 6)
            qp.drawEllipse(332, 292, 6, 6)

            qp.setBrush(Qt.red)
            qp.drawEllipse(302, 332, 6, 6)
            qp.drawEllipse(312, 332, 6, 6)
            qp.drawEllipse(322, 332, 6, 6)

            qp.setBrush(Qt.green)
            qp.drawEllipse(262, 302, 6, 6)
            qp.drawEllipse(262, 312, 6, 6)
            qp.drawEllipse(262, 322, 6, 6)

            self.single_0_0 = False
            self.single_0_1 = True

        else:
            qp.setPen(Qt.black)
            qp.setBrush(Qt.green)

            qp.drawEllipse(272, 262, 6, 6)
            qp.drawEllipse(282, 262, 6, 6)
            qp.drawEllipse(292, 262, 6, 6)

            qp.setBrush(Qt.red)
            qp.drawEllipse(332, 272, 6, 6)
            qp.drawEllipse(332, 282, 6, 6)
            qp.drawEllipse(332, 292, 6, 6)

            qp.setBrush(Qt.green)
            qp.drawEllipse(302, 332, 6, 6)
            qp.drawEllipse(312, 332, 6, 6)
            qp.drawEllipse(322, 332, 6, 6)

            qp.setBrush(Qt.red)
            qp.drawEllipse(262, 302, 6, 6)
            qp.drawEllipse(262, 312, 6, 6)
            qp.drawEllipse(262, 322, 6, 6)

            self.single_0_0 = True
            self.single_0_1 = False

    def propose(self, veh_id, current, origin, destination, speed, current_time, pattern, sendData):
        server_address = ('localhost', 6789)
        max_size = 4096

        # print('Starting the client at', datetime.now())

        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sendData_1["pattern"] = pattern
        current_position = list(current)
        # print('++++++++++++++++++++++++++++++++++++++')
        self.sendData_1["origin"] = list(origin)
        self.sendData_1["destination"] = list(destination)
        self.sendData_1["speed"] = speed

        # sendData_1: veh info and current Total_time
        dictMerge = dict({"time_step": current_time}, **sendData)
        dictMerge = dict({"current_position": current_position}, **dictMerge)
        mes = bytes(json.dumps(dictMerge), encoding='utf-8')
        # print(dictMerge)

        client.sendto(mes, server_address)
        data, server = client.recvfrom(max_size)

        data = data.decode('utf-8')
        recData = json.loads(data)
        # print('At', datetime.now(), server, 'said', recData)
        client.close()
        self.my_result = recData['result']

        return self.my_result

    def drawVehicles(self, qp):

        qp.setPen(Qt.black)
        qp.setBrush(Qt.green)

        # Vehicles Pattern2(from N5 to S5)
        for i, veh in enumerate(self.vehicles_N):
            if (veh.getPosition().x + veh.getSpeed().x, veh.getPosition().y + veh.getSpeed().y) in self.collision_check_N:
                qp.drawRect(veh.getPosition().x, veh.getPosition().y, veh.getSize().x, veh.getSize().y)
                for i in range(11):
                    self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y - i))
            else:
                # Just before intersection
                if veh.getPosition().y + veh.getSpeed().y > 260 and veh.getPosition().y <= 260:
                   # Try to make a reservation from IM. If false, then stop before entering.
                    if self.propose(i, (veh.getPosition().x, veh.getPosition().y), (313, 270),
                                    (313, 330), veh.getSpeed().y, self.t_t, 2, self.sendData_2["vehicle"][i]):
                   # if False:
                        self.vehicles_N[i].getPosition().y += self.vehicles_N[i].getSpeed().y

                        if self.vehicles_N[i].getPosition().y > 600:
                            self.vehicles_N[i].getPosition().y = 0

                        qp.drawRect(self.vehicles_N[i].getPosition().x, self.vehicles_N[i].getPosition().y, 5, 10)
                        for i in range(11):
                            self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y - i))
                    else:
                        qp.drawRect(self.vehicles_N[i].getPosition().x, self.vehicles_N[i].getPosition().y, 5, 10)
                        for i in range(11):
                            self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y - i))
                else:
                    self.vehicles_N[i].getPosition().y += self.vehicles_N[i].getSpeed().y

                    if self.vehicles_N[i].getPosition().y > 600:
                        self.vehicles_N[i].getPosition().y = 0

                    qp.drawRect(self.vehicles_N[i].getPosition().x, self.vehicles_N[i].getPosition().y, 5, 10)
                    for i in range(5):
                        self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y - i))

        # Vehicles Pattern1(from W1 to S6)
        for i, veh in enumerate(self.vehicles_W):
            # Check if there are vehicles ahead. If true, stop
            if (veh.getPosition().x + veh.getSpeed().x, veh.getPosition().y + veh.getSpeed().y) in self.collision_check_W:
                qp.drawRect(veh.getPosition().x, veh.getPosition().y, veh.getSize().x, veh.getSize().y)
                # Make the room not available for other vehicles
                for j in range(11):
                    self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))
            # Move forward
            else:
                # Just before the intersection
                if veh.getPosition().x + 10 + veh.getSpeed().x > 270 and veh.getPosition().x <= 270 - 10:
                    # Check traffic signal. True, then stop before entering.
                    if not self.propose(i, (veh.getPosition().x, veh.getPosition().y), (270, 273), (330, 330), veh.getSpeed().x, self.t_t, 1, self.sendData_1["vehicle"][i]):
                    # if False:
                        # print("False", (veh.getPosition().x, veh.getPosition().y))
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
                        for j in range(11):
                            self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))
                    # Enter intersection
                    else:
                        # print("True", (veh.getPosition().x, veh.getPosition().y))
                        veh.getPosition().x += veh.getSpeed().x
                        print(self.t_t, veh.getPosition().x, veh.getPosition().y)
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
                        for j in range(11):
                            self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))

                else:
                    # Already in the intersection
                    if 270 < veh.getPosition().x < 328 and veh.getPosition().y < 330:
                        qp.save()
                        qp.translate(veh.getPosition().x, veh.getPosition().y)

                        # Calculate rotation angle
                        if ((veh.getPosition().x - 270 + veh.getSpeed().x) / 60) * 90 > 15:
                            self.r[i] = ((veh.getPosition().x - 270 + veh.getSpeed().x) / 60) * 90
                            qp.rotate(self.r[i])
                        elif ((veh.getPosition().x - 270 + veh.getSpeed().x) / 60) * 90 > 90:
                            self.r[i] = 90
                            qp.rotate(self.r[i])
                        else:
                            self.r[i] = 0
                            qp.rotate(self.r[i])
                        qp.translate(-veh.getPosition().x, -veh.getPosition().y)

                        # Calculate trajectory by using Bezier Curve
                        x = pow(1 - (self.beze_t[i] / 60), 2) * 273 + 2 * (self.beze_t[i] / 60) * (
                        1 - self.beze_t[i] / 60) * 330 + pow(
                            self.beze_t[i] / 60, 2) * 330
                        y = pow(1 - (self.beze_t[i] / 60), 2) * 273 + 2 * (self.beze_t[i] / 60) * (
                        1 - self.beze_t[i] / 60) * 273 + pow(
                            self.beze_t[i] / 60, 2) * 330
                        veh.setPosition(Position(x, y))

                        self.beze_t[i] += 2
                        print(self.t_t, veh.getPosition().x, veh.getPosition().y)
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
                        for j in range(11):
                            self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))
                        qp.restore()

                    # Already left intersection
                    elif 328 <= veh.getPosition().x and veh.getPosition().y < 600:
                        qp.save()
                        qp.translate(veh.getPosition().x, veh.getPosition().y)
                        qp.rotate(90)
                        qp.translate(-veh.getPosition().x, -veh.getPosition().y)
                        veh.getPosition().y += veh.getSpeed().x
                        print(self.t_t, veh.getPosition().x, veh.getPosition().y)
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
                        for j in range(11):
                            self.collision_check_W.append((veh.getPosition().x, veh.getPosition().y - j))
                        qp.restore()

                    # Already left screen
                    elif veh.getPosition().y >= 600:
                        veh.getPosition().x = 0
                        veh.getPosition().y = 273
                        self.beze_t[i] = 2
                        print(self.t_t, veh.getPosition().x, veh.getPosition().y)
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
                        for j in range(11):
                            self.collision_check_W.append((veh.getPosition().x, veh.getPosition().y - j))

                    # Move horizontal direction(across X_axis)
                    else:
                        veh.getPosition().x += veh.getSpeed().x
                        print(self.t_t, veh.getPosition().x, veh.getPosition().y)
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
                        for j in range(11):
                            self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))

        # Vehicle Pattern3(From E4 to W4)
        # for i, veh in enumerate(vehicles_E):
        #     if 330 <= vehicles_E[0].getPosition().x and vehicles_E[0].getPosition().x - vehicles_E[0].getSpeed().x < 330:
        #         if self.propose(0, (vehicles_E[0].getPosition().x, vehicles_E[0].getPosition().y), (330, 313), (270, 313), veh.getSpeed().x, self.t_t, 3, self.sendData_3["vehicle"][0]):
        #         # if True:
        #             self.vehicles_E[0].getPosition().x -= self.vehicles_E[0].getSpeed().x
        #
        #             if self.vehicles_E[0].getPosition().x < 0:
        #                 self.vehicles_E[0].getPosition().x = 600
        #
        #             qp.drawPoint(self.vehicles_E[0].getPosition().x + 1, self.vehicles_E[0].getPosition().y - 1)
        #             qp.drawRect(self.vehicles_E[0].getPosition().x, self.vehicles_E[0].getPosition().y, 10, 5)
        #         else:
        #             qp.drawRect(self.vehicles_E[0].getPosition().x, self.vehicles_E[0].getPosition().y, 10, 5)
        #     else:
        #         self.vehicles_E[0].getPosition().x -= self.vehicles_E[0].getSpeed().x
        #
        #         if self.vehicles_E[0].getPosition().x < 0:
        #             self.vehicles_E[0].getPosition().x = 600
        #
        #         qp.drawRect(self.vehicles_E[0].getPosition().x, self.vehicles_E[0].getPosition().y, 10, 5)

        for i, veh in enumerate(self.vehicles_E):
            if (veh.getPosition().x + veh.getSpeed().x,
                veh.getPosition().y + veh.getSpeed().y) in self.collision_check_E:
                qp.drawRect(veh.getPosition().x, veh.getPosition().y, veh.getSize().x, veh.getSize().y)
                for j in range(16):
                    self.collision_check_E.append((veh.getPosition().x + j, veh.getPosition().y))
            else:
                if 330 <= veh.getPosition().x and veh.getPosition().x - veh.getSpeed().x < 330:
                    if self.propose(i, (veh.getPosition().x, veh.getPosition().y), (330, 313), (270, 313), veh.getSpeed().x, self.t_t, 3, self.sendData_3["vehicle"][i]):
                    # if True:
                        self.vehicles_E[i].getPosition().x -= self.vehicles_E[i].getSpeed().x

                        if self.vehicles_E[i].getPosition().x < 0:
                            self.vehicles_E[i].getPosition().x = 600

                        qp.drawPoint(self.vehicles_E[i].getPosition().x + 1, self.vehicles_E[i].getPosition().y - 1)
                        qp.drawRect(self.vehicles_E[i].getPosition().x, self.vehicles_E[i].getPosition().y, 10, 5)
                        for j in range(16):
                            self.collision_check_E.append((veh.getPosition().x + j, veh.getPosition().y))
                    else:
                        qp.drawRect(self.vehicles_E[i].getPosition().x, self.vehicles_E[i].getPosition().y, 10, 5)
                        for j in range(16):
                            self.collision_check_E.append((veh.getPosition().x + j, veh.getPosition().y))
                else:
                    self.vehicles_E[i].getPosition().x -= self.vehicles_E[i].getSpeed().x

                    if self.vehicles_E[i].getPosition().x < 0:
                        self.vehicles_E[i].getPosition().x = 600

                    qp.drawRect(self.vehicles_E[i].getPosition().x, self.vehicles_E[i].getPosition().y, 10, 5)
                    for j in range(16):
                        self.collision_check_E.append((veh.getPosition().x + j, veh.getPosition().y))

        # Vehicle Pattern4(From S3 to W4)
        for i, veh in enumerate(vehicles_S3_W4):
            # print(vehicles_S3_W4)
            # print('**********************')
            # Check if there are vehicles ahead. If true, stop
            if (veh.getPosition().x + veh.getSpeed().x, veh.getPosition().y - veh.getSpeed().y) in self.collision_check_S:
                qp.drawRect(veh.getPosition().x, veh.getPosition().y, veh.getSize().x, veh.getSize().y)
                # Make the room not available for other vehicles
                for j in range(11):
                    self.collision_check_S.append((veh.getPosition().x, veh.getPosition().y + j))
            # Move forward
            else:
                # Just before the intersection
                if veh.getPosition().y - veh.getSpeed().y < 330 and veh.getPosition().y >= 330:
                    # Make Propose
                    if not self.propose(i, (veh.getPosition().x, veh.getPosition().y), (293, 330), (270, 306),
                                        veh.getSpeed().y, self.t_t, 4, self.sendData_4["vehicle"][i]):
                    # if False:
                        print(self.t_t, "False", (veh.getPosition().x, veh.getPosition().y))
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
                        for j in range(11):
                            self.collision_check_S.append((veh.getPosition().x, veh.getPosition().y + j))
                    # Enter intersection
                    else:
                        print('number', i)
                        print(self.t_t, "True", (veh.getPosition().x, veh.getPosition().y))
                        veh.getPosition().y -= veh.getSpeed().y
                        # print((veh.getPosition().x, veh.getPosition().y))
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
                        for j in range(11):
                            self.collision_check_W.append((veh.getPosition().x, veh.getPosition().y + j))

                else:
                    # Already in the intersection
                    # Later should consider 260 < veh.getPosition().x < 293
                    if 270 < veh.getPosition().x <= 293 and veh.getPosition().y < 330:
                        if veh.getPosition().y > 320:
                            x = veh.getPosition().x
                            y = veh.getPosition().y - veh.getSpeed().y

                            veh.setPosition(Position(x, y))
                            qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
                            for j in range(11):
                                self.collision_check_W.append((veh.getPosition().x, veh.getPosition().y + j))
                        else:
                            qp.save()
                            qp.translate(veh.getPosition().x, veh.getPosition().y)

                            # Calculate rotation angle
                            if ((330 - veh.getPosition().y - veh.getSpeed().y) / 22) * 90 > 15:
                                self.S3_W4_r[i] = ((330 - veh.getPosition().y - veh.getSpeed().y) / 22) * 90
                                qp.rotate(-self.S3_W4_r[i])
                            else:
                                self.S3_W4_r[i] = 0
                                qp.rotate(self.S3_W4_r[i])
                            qp.translate(-veh.getPosition().x, -veh.getPosition().y)

                            # Calculate trajectory by using Bezier Curve
                            x = pow(1 - (self.S3_W4_beze_t[i] / 22), 2) * 293 + 2 * (self.S3_W4_beze_t[i] / 22) * (
                                1 - self.S3_W4_beze_t[i] / 22) * 293 + pow(
                                self.S3_W4_beze_t[i] / 22, 2) * 270
                            y = pow(1 - (self.S3_W4_beze_t[i] / 22), 2) * 320 + 2 * (self.S3_W4_beze_t[i] / 22) * (
                                1 - self.S3_W4_beze_t[i] / 22) * 306 + pow(
                                self.S3_W4_beze_t[i] / 22, 2) * 306

                            veh.setPosition(Position(x, y))

                            self.S3_W4_beze_t[i] += 2
                            qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
                            for j in range(11):
                                self.collision_check_W.append((veh.getPosition().x, veh.getPosition().y + j))
                            qp.restore()

                        # Calculate the big Square's coordinate
                        # self.S3_W4_up_left_x[i] = rec_funcs.S2W_up_left_x(veh.getPosition().x)
                        # self.S3_W4_up_left_y[i] = rec_funcs.S2W_up_left_y(veh.getPosition().y, self.S3_W4_r[i])
                        # self.S3_W4_down_left_x[i] = rec_funcs.S2W_down_left_x(veh.getPosition().x)
                        # self.S3_W4_down_left_y[i] = rec_funcs.S2W_down_left_y(veh.getPosition().y, self.S3_W4_r[i])
                        # self.S3_W4_up_right_x[i] = rec_funcs.S2W_up_right_x(veh.getPosition().x, self.S3_W4_r[i])
                        # self.S3_W4_up_right_y[i] = rec_funcs.S2W_up_right_y(veh.getPosition().y, self.S3_W4_r[i])
                        # self.S3_W4_down_right_x[i] = rec_funcs.S2W_down_right_x(veh.getPosition().x, self.S3_W4_r[i])
                        # self.S3_W4_down_right_y[i] = rec_funcs.S2W_down_right_y(veh.getPosition().y, self.S3_W4_r[i])


                    # Already left intersection
                    elif -10 < veh.getPosition().x <= 270:
                        qp.save()
                        qp.translate(veh.getPosition().x, veh.getPosition().y)
                        qp.rotate(-90)
                        qp.translate(-veh.getPosition().x, -veh.getPosition().y)
                        veh.getPosition().x -= veh.getSpeed().y
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
                        for j in range(11):
                            self.collision_check_S.append((veh.getPosition().x + j, veh.getPosition().y))
                        qp.restore()

                    # Already left screen
                    elif veh.getPosition().x <= -10:
                        veh.getPosition().x = 293
                        veh.getPosition().y = 600
                        self.S3_W4_beze_t[i] = 0
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
                        for j in range(11):
                            self.collision_check_S.append((veh.getPosition().x, veh.getPosition().y + j))

                    # Move vertical direction(across Y_axis)
                    else:
                        veh.getPosition().y -= veh.getSpeed().y
                        qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
                        for j in range(11):
                            self.collision_check_S.append((veh.getPosition().x, veh.getPosition().y + j))


        self.collision_check = []
        self.collision_check_N = []
        self.collision_check_S = []
        self.collision_check_W = []
        self.collision_check_E = []

        self.ti += 10
        if self.ti > 700:
            self.ti = 0
            # print(self.t.elapsed())
            self.t.restart()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Vehicles from North5 to South5
    vehicles_N5_S5 = []
    # for i in range(5):
    #     v = Vehicle()
    #     v.setPosition(Position(313, 0 - i * 20))
    #     v.setSpeed(Speed(0, 2))
    #     v.setSize(Size(5, 10))
    #     vehicles_N5_S5.append(v)
    v = Vehicle()
    v.setPosition(Position(313, 0 - 2 * 20))
    v.setSpeed(Speed(0, 2))
    v.setSize(Size(5, 10))
    vehicles_N5_S5.append(v)

    v = Vehicle()
    v.setPosition(Position(313, 0 - 2 * 40))
    v.setSpeed(Speed(0, 2))
    v.setSize(Size(5, 10))
    vehicles_N5_S5.append(v)

    v = Vehicle()
    v.setPosition(Position(313, 0 - 2 * 60))
    v.setSpeed(Speed(0, 2))
    v.setSize(Size(5, 10))
    vehicles_N5_S5.append(v)



    # ***************************************************
    # Vehicles from South3 to West4
    vehicles_S3_W4 = []
    # for i in range(3):
    #     v = Vehicle()
    #     v.setPosition(Position(293, 600 + i * 20))
    #     v.setSpeed(Speed(0, 2))
    #     v.setSize(Size(5, 10))
    #     vehicles_S3_W4.append(v)
    v = Vehicle()
    v.setPosition(Position(293, 600 + 2 * 20))
    v.setSpeed(Speed(0, 2))
    v.setSize(Size(5, 10))
    vehicles_S3_W4.append(v)

    v = Vehicle()
    v.setPosition(Position(293, 600 + 2 * 50))
    v.setSpeed(Speed(0, 2))
    v.setSize(Size(5, 10))
    vehicles_S3_W4.append(v)

    v = Vehicle()
    v.setPosition(Position(293, 600 + 2 * 80))
    v.setSpeed(Speed(0, 2))
    v.setSize(Size(5, 10))
    vehicles_S3_W4.append(v)

    v = Vehicle()
    v.setPosition(Position(293, 600 + 2 * 100))
    v.setSpeed(Speed(0, 2))
    v.setSize(Size(5, 10))
    vehicles_S3_W4.append(v)


    # ***************************************************
    # Vehicles from West1 to South6
    vehicles_W1_S6 = []
    # for i in range(10):
    #     v = Vehicle()
    #     v.setPosition(Position(0 - i * 20, 273))
    #     v.setSpeed(Speed(2, 0))
    #     v.setSize(Size(10, 5))
    #     vehicles_W1_S6.append(v)
    v = Vehicle()
    v.setPosition(Position(0, 273))
    v.setSpeed(Speed(2, 0))
    v.setSize(Size(10, 5))
    vehicles_W1_S6.append(v)

    v = Vehicle()
    v.setPosition(Position(0 - 2 * 40, 273))
    v.setSpeed(Speed(2, 0))
    v.setSize(Size(10, 5))
    vehicles_W1_S6.append(v)

    v = Vehicle()
    v.setPosition(Position(0 - 2 * 50, 273))
    v.setSpeed(Speed(2, 0))
    v.setSize(Size(10, 5))
    vehicles_W1_S6.append(v)

    # v = Vehicle()
    # v.setPosition(Position(0 - 2 * 80, 273))
    # v.setSpeed(Speed(2, 0))
    # v.setSize(Size(10, 5))
    # vehicles_W1_S6.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(0 - 2 * 100, 273))
    # v.setSpeed(Speed(2, 0))
    # v.setSize(Size(10, 5))
    # vehicles_W1_S6.append(v)

    # ***************************************************
    # Vehicles from East
    vehicles_E = []
    v = Vehicle()
    v.setPosition(Position(600, 313))
    v.setSpeed(Speed(3, 0))
    v.setSize(Size(10, 5))
    vehicles_E.append(v)

    v = Vehicle()
    v.setPosition(Position(600 + 2 * 20, 313))
    v.setSpeed(Speed(3, 0))
    v.setSize(Size(10, 5))
    vehicles_E.append(v)

    v = Vehicle()
    v.setPosition(Position(600 + 2 * 40, 313))
    v.setSpeed(Speed(3, 0))
    v.setSize(Size(10, 5))
    vehicles_E.append(v)

    v = Vehicle()
    v.setPosition(Position(600 + 2 * 80, 313))
    v.setSpeed(Speed(3, 0))
    v.setSize(Size(10, 5))
    vehicles_E.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(600 + 2 * 100, 313))
    # v.setSpeed(Speed(3, 0))
    # v.setSize(Size(10, 5))
    # vehicles_E.append(v)
    #
    # v = Vehicle()
    # v.setPosition(Position(600 + 2 * 110, 313))
    # v.setSpeed(Speed(3, 0))
    # v.setSize(Size(10, 5))
    # vehicles_E.append(v)

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

    ex = Example(vehicles_N5_S5, vehicles_W1_S6, vehicles_E, vehicles_S3_W4, sendData_1, sendData_2, sendData_3, sendData_4)

    sys.exit(app.exec_())