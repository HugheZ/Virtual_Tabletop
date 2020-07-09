from virtual_tabletop.Connections import FirebaseConnector
from PyQt5 import QtWidgets, QtGui
from virtual_tabletop.UI.MainWindow import MainWindow
from virtual_tabletop.Data.GameCollection import GameCollection
from os import sys, path
import json
from getpass import getpass

def launch():
    app = QtWidgets.QApplication(sys.argv)

    #check environment
    count = len(QtGui.QGuiApplication.screens())
    if count < 2:
        raise EnvironmentError('Desktop count below minimum required number\nExpected >=2 but received ' + str(count))

    #create files if needed
    if not path.exists('config.json'):
        with open('config.json','w') as f:
            config = {
                "key_path":None,
                "savedir": path.join('.','localboards'),
                "storecreds":False,
                "auto_upload":False,
                "store_on_download":False,
                "login_on_startup":False
            }
            json.dump(config, f, indent=3)

    #open window
    window = MainWindow()

    window.show()
    sys.exit(app.exec())

