from virtual_tabletop.Connections import FirebaseConnector
from PyQt5 import QtWidgets
from virtual_tabletop.UI.MainWindow import MainWindow
from virtual_tabletop.Data.GameCollection import GameCollection
from os import sys, path
import json
from getpass import getpass

def launch():
    app = QtWidgets.QApplication(sys.argv)

    #credentials
    key = None
    email = None
    password = None
    savedir = path.join('.','localboards')

    #open configuration file
    if path.exists('config.json'):
        config = json.load(open('config.json'))
        key = config.get('key_path')
        email = config.get('email')
        password = config.get('password')
        savedir = config.get('savedir')

    #link connector
    connector = None
    if path.exists(key):
        connector = FirebaseConnector.Connector(key=key, email=email, password=password, savedir=savedir)

    window = MainWindow(source=connector)

    window.show()
    sys.exit(app.exec())

