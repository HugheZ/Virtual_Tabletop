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
        with open('config.json') as f:
            config = json.load(f)
            key = config.get('key_path')
            email = config.get('email')
            password = config.get('password')
            savedir = config.get('savedir')
    else:
        with open('config.json','w') as f:
            config = {
                "key_path":None,
                "savedir":"./localboards",
                "storecreds":False,
                "storecreds":False,
                "auto_upload":False,
                "store_on_download":False,
                "login_on_startup":False
            }
            json.dump(config, f)

    #link connector
    connector = None
    if path.exists(key):
        connector = FirebaseConnector.Connector(key=key, email=email, password=password, savedir=savedir)

    window = MainWindow(source=connector)

    window.show()
    sys.exit(app.exec())

