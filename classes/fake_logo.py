import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog, QApplication, QFileDialog
# from classes.home import HomeScreen
from classes.smart_desk import SmartDesk
from classes.object_motion import ObjectMotionPre
from global_var import widget, fakeLogo_file, PRESSED_STYLE, DEFAULT_STYLE
from FeatureMatching.FakeLogoDetection import FakeLogosDetection

class FakeLogoDet(QDialog):
    def __init__(self):
        super(FakeLogoDet, self).__init__()
        self.cameraon = False
        self.photouploadon = False
        self.fname = ["", ""]
        self.logo = None
        loadUi(fakeLogo_file, self)
        self.backButton.clicked.connect(self.backward)
        self.camera.clicked.connect(self.opencamera)
        self.uploadFile.clicked.connect(self.upload)
        self.startButton.clicked.connect(self.start)

    def opencamera(self):
        if self.cameraon:
            self.reset()
        else:
            self.photouploadon = False
            self.cameraon = True
            self.uploadFile.setStyleSheet(DEFAULT_STYLE)
            self.camera.setStyleSheet(PRESSED_STYLE)
            self.error.setText("")
            self.file_name.setText("")
            self.file_name_2.setText("")
            # 
            self.logo, __ = QFileDialog.getOpenFileName(self, "Upload logo", "C:/Users/", 'Images(*.PNG *.JPG *.JPEG)')
            self.file_name_3.setText(self.logo)

    def upload(self):
        if self.photouploadon:
            self.reset()
        else:
            self.cameraon = False
            self.photouploadon = True
            self.camera.setStyleSheet(DEFAULT_STYLE)
            self.uploadFile.setStyleSheet(PRESSED_STYLE)
            self.file_name_3.setText("")
            self.error.setText("")
            # Open the image from the file explore and define the file name (stored in "self.fname")
            self.fname[0], __ = QFileDialog.getOpenFileName(self, "Upload Images 1", "C:/Users/", 'Images(*.PNG *.JPG *.JPEG)')
            self.fname[1], __ = QFileDialog.getOpenFileName(self, "Upload Images 2", "C:/Users/", 'Images(*.PNG *.JPG *.JPEG)')
            self.file_name.setText(self.fname[0]) # Change the label below the button to the file name
            self.file_name_2.setText(self.fname[1]) # Change the label below the button to the file name

    # "Start" Button Function
    def start(self):
        # Call the real-time feature matching
        if self.cameraon and len(self.logo) != 0:
            print("Compare using Camera") # <-- The method should be here
            detector = FakeLogosDetection()
            input_image, input_keypoints, input_descriptors = detector.load_image(img1_path=self.logo)
            detector.real_time_matching(input_image, input_keypoints, input_descriptors)
        # Call the feature matching between two images
        elif self.photouploadon and len(self.fname) != 0:
            
            print("Compare between two images") # <-- The method should be here
            detector = FakeLogosDetection()

            img_kp1, img_kp2 = detector.load_image(img1_path=self.fname[0],
                                                    img2_path=self.fname[1])

            matching = detector.compute_matches(
                des_image1=img_kp1[2], des_image2=img_kp2[2])

            detector.image_to_image_matching(
                img_kp1[0], img_kp1[1], img_kp2[0], img_kp2[1], matching)

        # Error massage 
        else:
            self.error.setText("* No argument have been selected")
        self.reset()

    # "Go Back" Button Function, Return back to the home screen
    def backward(self):
        self.reset()
        self.error.setText("")
        widget.setCurrentIndex(widget.currentIndex() -1)

    def reset(self):
        self.file_name.setText("")
        self.file_name_2.setText("")
        self.file_name_3.setText("")
        self.fname = ["", ""]
        self.logo = None
        self.cameraon = False
        self.photouploadon = False
        self.camera.setStyleSheet(DEFAULT_STYLE)
        self.uploadFile.setStyleSheet(DEFAULT_STYLE)