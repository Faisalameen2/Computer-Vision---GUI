import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog, QApplication, QFileDialog
# from home import HomeScreen
# from fake_logo import FakeLogoDet
from classes.smart_desk import SmartDesk
from DenseMotionEstimation.ObjectMovmentPrediction import ObjectMovmentDetection

APP_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(APP_ROOT)
from global_var import widget, objectMotion_file, PRESSED_STYLE, DEFAULT_STYLE



class ObjectMotionPre(QDialog):
    def __init__(self):
        super(ObjectMotionPre, self).__init__()
        loadUi(objectMotion_file, self)
        self.videouploadon = False
        self.fname = None
        self.uploadFile.clicked.connect(self.upload)
        self.startButton.clicked.connect(self.start)
        self.backButton.clicked.connect(self.backward)

    # "Upload Video" Button Function
    def upload(self):
        if self.videouploadon:
            self.reset()
        else:
            self.videouploadon = True
            self.uploadFile.setStyleSheet(PRESSED_STYLE)
            # Open the video from the file explore and define the file name (stored in "self.fname")
            self.fname, __ = QFileDialog.getOpenFileName(self, "Open File", "C:/Users/Arab0/Documents", 'Videos(*.MP4 *.WAV)')
            self.file_name.setText(self.fname) # Change the label below the button to the file name

    # "Start" Button Function
    def start(self):
        if self.videouploadon and len(self.fname) != 0:
            denseMotion = ObjectMovmentDetection()
            denseMotion.video_motion_estimation(
                video_file_path=self.fname)
        else:
            self.error.setText("* No argument have been selected")
        self.reset()

    # "Go Back" Button Function, Return back to the home screen
    def backward(self):
        self.reset()
        self.error.setText("")
        widget.setCurrentIndex(widget.currentIndex() -2)

    def reset(self):
        self.file_name.setText("")
        self.fname = None
        self.videouploadon = False
        self.uploadFile.setStyleSheet(DEFAULT_STYLE)