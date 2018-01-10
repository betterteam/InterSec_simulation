from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFrame, QDesktopWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QTimer, QTime


def drawLines(qp):
    # print(self.t.elapsed())

    pen = QPen(Qt.black, 2, Qt.SolidLine)
    pen_dash = QPen(Qt.black, 2, Qt.DotLine)

    # IM1 Vertical
    qp.setPen(pen)
    # qp.drawLine(270, 0, 270, 600)
    #
    # qp.drawLine(330, 0, 330, 600)
    # qp.drawLine(300, 0, 300, 270)
    # qp.drawLine(300, 330, 300, 600)

    qp.setPen(pen_dash)
    qp.drawLine(280, 330, 280, 600)
    qp.drawLine(290, 330, 290, 600)
    qp.drawLine(310, 330, 310, 600)
    qp.drawLine(320, 330, 320, 600)
    #
    qp.drawLine(280, 0, 280, 270)
    qp.drawLine(290, 0, 290, 270)
    qp.drawLine(310, 0, 310, 270)
    qp.drawLine(320, 0, 320, 270)

    # IM1 Tropical
    qp.setPen(pen)
    # qp.drawLine(0, 270, 600, 270)
    #
    # qp.drawLine(0, 330, 600, 330)
    # qp.drawLine(0, 300, 270, 300)
    #
    # qp.drawLine(330, 300, 600, 300)

    qp.setPen(pen_dash)
    qp.drawLine(0, 280, 270, 280)
    qp.drawLine(0, 290, 270, 290)
    qp.drawLine(0, 310, 270, 310)
    qp.drawLine(0, 320, 270, 320)
    #
    qp.drawLine(330, 280, 600, 280)
    qp.drawLine(330, 290, 600, 290)
    qp.drawLine(330, 310, 600, 310)
    qp.drawLine(330, 320, 600, 320)

    # IM2 Vertical
    qp.setPen(pen)
    qp.drawLine(600, 0, 600, 600)
    qp.drawLine(660, 0, 660, 600)

    qp.drawLine(630, 0, 630, 270)
    qp.drawLine(630, 330, 630, 600)

    qp.setPen(pen_dash)

    qp.drawLine(610, 0, 610, 270)
    qp.drawLine(620, 0, 620, 270)
    qp.drawLine(640, 0, 640, 270)
    qp.drawLine(650, 0, 650, 270)

    qp.drawLine(610, 330, 610, 600)
    qp.drawLine(620, 330, 620, 600)
    qp.drawLine(640, 330, 640, 600)
    qp.drawLine(650, 330, 650, 600)

    # IM2 Tropical
    qp.setPen(pen)
    qp.drawLine(600, 270, 930, 270)
    qp.drawLine(600, 330, 930, 330)

    qp.drawLine(660, 300, 930, 300)

    # qp.setPen(pen_dash)
    # qp.drawLine(660, 280, 930, 280)
    # qp.drawLine(660, 290, 930, 290)
    # qp.drawLine(660, 310, 930, 310)
    # qp.drawLine(660, 320, 930, 320)

    # IM3 Vertical
    qp.setPen(pen)
    qp.drawLine(270, 600, 270, 930)

    qp.drawLine(330, 600, 330, 930)
    qp.drawLine(300, 660, 300, 930)
    qp.drawLine(300, 660, 300, 930)

    # qp.setPen(pen_dash)
    # qp.drawLine(280, 660, 280, 930)
    # qp.drawLine(290, 660, 290, 930)
    # qp.drawLine(310, 660, 310, 930)
    # qp.drawLine(320, 660, 320, 930)

    # IM3 Tropical
    qp.setPen(pen)
    qp.drawLine(0, 600, 600, 600)

    qp.drawLine(0, 660, 600, 660)
    qp.drawLine(0, 630, 270, 630)

    qp.drawLine(330, 630, 600, 630)

    # qp.setPen(pen_dash)
    # qp.drawLine(0, 610, 270, 610)
    # qp.drawLine(0, 620, 270, 620)
    # qp.drawLine(0, 640, 270, 640)
    # qp.drawLine(0, 650, 270, 650)
    #
    # qp.drawLine(330, 610, 600, 610)
    # qp.drawLine(330, 620, 600, 620)
    # qp.drawLine(330, 640, 600, 640)
    # qp.drawLine(330, 650, 600, 650)

    # IM4 Vertical
    qp.setPen(pen)
    qp.drawLine(600, 600, 600, 930)
    qp.drawLine(660, 600, 660, 930)

    qp.drawLine(630, 660, 630, 930)
    # qp.drawLine(630, 330, 630, 600)

    # qp.setPen(pen_dash)
    #
    # qp.drawLine(610, 660, 610, 930)
    # qp.drawLine(620, 660, 620, 930)
    # qp.drawLine(640, 660, 640, 930)
    # qp.drawLine(650, 660, 650, 930)

    # qp.drawLine(610, 330, 610, 600)
    # qp.drawLine(620, 330, 620, 600)
    # qp.drawLine(640, 330, 640, 600)
    # qp.drawLine(650, 330, 650, 600)

    # IM4 Tropical
    qp.setPen(pen)
    qp.drawLine(600, 600, 930, 600)
    qp.drawLine(600, 660, 930, 660)

    qp.drawLine(660, 630, 930, 630)

    # qp.setPen(pen_dash)
    # qp.drawLine(660, 610, 930, 610)
    # qp.drawLine(660, 620, 930, 620)
    # qp.drawLine(660, 640, 930, 640)
    # qp.drawLine(660, 650, 930, 650)








    # # IM1 Vertical
    # qp.setPen(pen)
    # qp.drawLine(270, 0, 270, 560)
    #
    # qp.drawLine(290, 0, 290, 560)
    # qp.drawLine(280, 0, 280, 270)
    # qp.drawLine(280, 290, 280, 560)
    #
    # # IM1 Tropical
    # qp.drawLine(0, 270, 560, 270)
    #
    # qp.drawLine(0, 280, 270, 280)
    # qp.drawLine(0, 290, 270, 290)
    #
    # qp.drawLine(290, 280, 560, 280)
    # qp.drawLine(270, 290, 560, 290)

