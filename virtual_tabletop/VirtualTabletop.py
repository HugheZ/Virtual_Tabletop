from virtual_tabletop.Connections import FirebaseConnector
from PyQt5 import QtWidgets
from virtual_tabletop.UI.MainWindow import MainWindow
from os import sys

class VT:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)

        window = MainWindow()
        window.show()
        app.exec()