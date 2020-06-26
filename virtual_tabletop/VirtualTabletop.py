from virtual_tabletop.Connections import FirebaseConnector
from PyQt5 import QtWidgets
from virtual_tabletop.UI.MainWindow import MainWindow
from virtual_tabletop.Data.GameCollection import GameCollection
from os import sys, path
import json
from getpass import getpass

def launch():
    app = QtWidgets.QApplication(sys.argv)

    #check environment
    desktop = QtWidgets.QDesktopWidget()
    if desktop.screenNumber() < 2:
        raise EnvironmentError('Desktop count below minimum required number')


    #credentials
    key = None
    email = None
    password = None
    savedir = path.join('.','localboards')

    #open configuration file
    if path.exists('config.json'):
        login = False
        storecreds = False
        with open('config.json') as f:
            config = json.load(f)
            key = config.get('key_path')
            savedir = config.get('savedir')
            login = config.get('login_on_startup')
            storecreds = config.get('storecreds')

        #get password and email if asked
        if storecreds and login:
            with open('credentials.json') as f:
                creds = json.load(f)
                email = creds.get('email')
                password = creds.get('password')
    else:
        with open('config.json','w') as f:
            config = {
                "key_path":None,
                "savedir": path.join('.','localboards'),
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

