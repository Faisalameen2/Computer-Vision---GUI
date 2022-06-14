import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog, QApplication
# from cv2 import CAP_PROP_XI_IMAGE_DATA_FORMAT_RGB32_ALPHA
APP_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(APP_ROOT)
from classes.fake_logo import FakeLogoDet
from classes.smart_desk import SmartDesk
from classes.object_motion import ObjectMotionPre
from global_var import widget, home_file, PRESSED_STYLE, DEFAULT_STYLE



screen1 = SmartDesk()

class HomeScreen(QDialog):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi(home_file, self)
        self.ch1 = False # will be toggled to True when the user choose Smart Desk
        self.ch2 = False # will be toggled to True when the user choose Fake Logo Detection
        self.ch3 = False # will be toggled to True when the user choose Object Motion Prediction
        self.nextButton.clicked.connect(self.nextscreen)
        self.facialRec.clicked.connect(self.choice1)
        self.featureMatching.clicked.connect(self.choice2)
        self.denseMotion.clicked.connect(self.choice3)


    # "Next" Button Function
    def nextscreen(self):
        if self.ch1:
            # Open a window for facial recognition (Smart Desk)
            screen1.start()
        elif  self.ch2:
            widget.setCurrentIndex(widget.currentIndex() + 1)
        elif self.ch3:
            widget.setCurrentIndex(widget.currentIndex() + 2)
        else:
            self.error.setText("* No argument have been selected")
        self.reset()

    # When the user choose Smart Desk
    def choice1(self):
        if self.ch1:
            self.reset()
        else:
            self.ch2 = False
            self.ch3 = False
            self.ch1 = True
            self.featureMatching.setStyleSheet(DEFAULT_STYLE)
            self.denseMotion.setStyleSheet(DEFAULT_STYLE)
            self.facialRec.setStyleSheet(PRESSED_STYLE)
            self.error.setText("")

    # When the user choose Fake Logo Detection
    def choice2(self):
        if self.ch2:
            self.reset()
        else:
            self.ch1 = False
            self.ch3 = False
            self.ch2 = True
            self.facialRec.setStyleSheet(DEFAULT_STYLE)
            self.denseMotion.setStyleSheet(DEFAULT_STYLE)
            self.featureMatching.setStyleSheet(PRESSED_STYLE)
            self.error.setText("")  

    # When the user choose Object Motion Prediction
    def choice3(self):
        if self.ch3:
            self.reset()
        else:
            self.ch1 = False
            self.ch2 = False
            self.ch3 = True
            self.facialRec.setStyleSheet(DEFAULT_STYLE)
            self.featureMatching.setStyleSheet(DEFAULT_STYLE) 
            self.denseMotion.setStyleSheet(PRESSED_STYLE)
            self.error.setText("")
    
    def reset(self):
        self.ch1 = False
        self.ch2 = False
        self.ch3 = False
        self.facialRec.setStyleSheet(DEFAULT_STYLE)
        self.featureMatching.setStyleSheet(DEFAULT_STYLE) 
        self.denseMotion.setStyleSheet(DEFAULT_STYLE)

