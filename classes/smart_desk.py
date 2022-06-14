import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog, QApplication
from FacialRecognition.SmartTable import SmartDisck
# from home import HomeWindow
# from fake_logo import FakeLogoDet
# from object_motion import ObjectMotionPre
# from main_app import widget

class SmartDesk(QDialog):
    def __init__(self):
        super(SmartDesk, self).__init__()


    def start(self):
        smartdisk = SmartDisck()
        smartdisk.real_time_recognition()
