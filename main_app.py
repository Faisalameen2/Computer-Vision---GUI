import sys
import os
from PyQt5 import uic
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog, QApplication
from classes.home import HomeScreen
from classes.smart_desk import SmartDesk
from classes.fake_logo import FakeLogoDet
from classes.object_motion import ObjectMotionPre

from global_var import widget, app
from os import environ

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

if __name__ == "__main__":
    suppress_qt_warnings()

home_screen = HomeScreen() 
widget.addWidget(home_screen)
screen2 = FakeLogoDet()
widget.addWidget(screen2)
screen3 = ObjectMotionPre()
widget.addWidget(screen3)
widget.setFixedHeight(720)
widget.setFixedWidth(1280)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Application is terminated")
