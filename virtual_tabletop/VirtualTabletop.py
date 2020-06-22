from virtual_tabletop.Connections import FirebaseConnector
from PyQt5 import QtWidgets
from virtual_tabletop.UI.MainWindow import MainWindow
from virtual_tabletop.Data.GameCollection import GameCollection
from os import sys
import json

class VT:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        self.connector = FirebaseConnector.Connector(key='key.json', email=input('Email: '), password=input('Password: '))

        self.window = MainWindow()
        
        self.data = self.connector.watch(self, self.getData)

        self.window.show()
        self.app.exec()
    
    def getData(self, data: GameCollection):
        '''Loads the retrieved data into a local copy and populates the UI\n
        data: the data retrieved from the firebase connector
        '''
        self.data = data
        self.__loadData()
    
    def __loadData(self):
        '''Transfers the loaded data to the UI
        '''
        self.window.loadLevel(self.data, '')

