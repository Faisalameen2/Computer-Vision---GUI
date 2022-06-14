from secrets import choice
import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog, QApplication
from os import environ


# Load the UI Files
cwd = os.getcwd()
home_file = os.path.join(cwd, "GUI/uiWindows/home_win.ui")
fakeLogo_file = os.path.join(cwd, "GUI/uiWindows/logo_win.ui")
objectMotion_file = os.path.join(cwd, "GUI/uiWindows/object_motion_win.ui")

# Setting the widget list and app for the GUI compnent
# Widget is a list of the UI windows
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

""" choices = 0


def setChoice(num):
    choices = 0
    choices = num

    return choices """

# Button Styles Constants
PRESSED_STYLE = """background: #CCCCCC;
                                        border: 2px solid #A39FA4;
                                        box-sizing: border-box;
                                        border-radius: 10px;

                                        font-family: 'Rockwell';
                                        font-style: normal;
                                        font-weight: 600;
                                        font-size: 18px;
                                        line-height: 25px;
                                        display: flex;
                                        align-items: center;
                                        text-align: center;

                                        color: #000000;"""

DEFAULT_STYLE = """background: #FFFFFF;
                   border: 2px solid #A39FA4;
                   box-sizing: border-box;
                   border-radius: 10px;
                   
                   font-family: 'Rockwell';
                   font-style: normal;
                   font-weight: 600;
                   font-size: 18px;
                   line-height: 25px;
                   display: flex;
                   align-items: center;
                   text-align: center;
                   color: #000000;"""